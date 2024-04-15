import json

import kubernetes

from ocp_resources.constants import TIMEOUT_4MINUTES
from ocp_resources.node import Node
from ocp_resources.resource import NamespacedResource
from timeout_sampler import TimeoutWatch


class ExecOnPodError(Exception):
    def __init__(self, command, rc, out, err):
        self.cmd = command
        self.rc = rc
        self.out = out
        self.err = err

    def __str__(self):
        return "Command execution failure: " f"{self.cmd}, " f"RC: {self.rc}, " f"OUT: {self.out}, " f"ERR: {self.err}"


class Pod(NamespacedResource):
    """
    Pod object, inherited from Resource.
    """

    api_version = NamespacedResource.ApiVersion.V1

    class Status(NamespacedResource.Status):
        CRASH_LOOPBACK_OFF = "CrashLoopBackOff"
        IMAGE_PULL_BACK_OFF = "ImagePullBackOff"
        ERR_IMAGE_PULL = "ErrImagePull"

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        teardown=True,
        privileged_client=None,
        yaml_file=None,
        delete_timeout=TIMEOUT_4MINUTES,
        **kwargs,
    ):
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            teardown=teardown,
            privileged_client=privileged_client,
            yaml_file=yaml_file,
            delete_timeout=delete_timeout,
            **kwargs,
        )

    @property
    def containers(self):
        """
        Get Pod containers

        Returns:
            list: List of Pod containers
        """
        return self.instance.spec.containers

    def execute(self, command, timeout=60, container=None, ignore_rc=False):
        """
        Run command on Pod

        Args:
            command (list): Command to run.
            timeout (int): Time to wait for the command.
            container (str): Container name where to exec the command.
            ignore_rc (bool): If True ignore error rc from the shell and return out.

        Returns:
            str: Command output.

        Raises:
            ExecOnPodError: If the command failed.
        """
        error_channel = {}
        stream_closed_error = "stream resp is closed"
        self.logger.info(f"Execute {command} on {self.name} ({self.node.name})")
        resp = kubernetes.stream.stream(
            api_method=self._kube_v1_api.connect_get_namespaced_pod_exec,
            name=self.name,
            namespace=self.namespace,
            command=command,
            container=container or self.containers[0].name,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
            _preload_content=False,
        )

        timeout_watch = TimeoutWatch(timeout=timeout)
        while resp.is_open():
            resp.run_forever(timeout=2)
            try:
                error_channel = json.loads(resp.read_channel(kubernetes.stream.ws_client.ERROR_CHANNEL))
                break
            except json.decoder.JSONDecodeError:
                # Check remaining time, in order to throw exception
                # if remaining time reached zero
                if timeout_watch.remaining_time() <= 0:
                    raise ExecOnPodError(command=command, rc=-1, out="", err=stream_closed_error)

        rcstring = error_channel.get("status")
        if rcstring is None:
            raise ExecOnPodError(command=command, rc=-1, out="", err=stream_closed_error)

        stdout = resp.read_stdout(timeout=5)
        stderr = resp.read_stderr(timeout=5)

        if rcstring == "Success" or ignore_rc:
            return stdout

        if rcstring == "Failure":
            raise ExecOnPodError(command=command, rc=-1, out="", err=error_channel)

        returncode = [
            int(cause["message"]) for cause in error_channel["details"]["causes"] if cause["reason"] == "ExitCode"
        ][0]

        raise ExecOnPodError(command=command, rc=returncode, out=stdout, err=stderr)

    def log(self, **kwargs):
        """
        Get Pod logs

        Returns:
            str: Pod logs.
        """
        return self._kube_v1_api.read_namespaced_pod_log(name=self.name, namespace=self.namespace, **kwargs)

    @property
    def node(self):
        """
        Get the node name where the Pod is running

        Returns:
            Node: Node
        """
        node_name = self.instance.spec.nodeName
        assert node_name, f"Node not found for pod {self.name}"
        return Node(
            client=self.privileged_client or self.client,
            name=node_name,
        )

    @property
    def ip(self):
        return self.instance.status.podIP
