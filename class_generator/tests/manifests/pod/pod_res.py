# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class Pod(NamespacedResource):
    """
    Pod is a collection of containers that can run on a host. This resource is
    created by clients and scheduled onto hosts.
    """

    api_version: str = NamespacedResource.ApiVersion.V1

    def __init__(
        self,
        active_deadline_seconds: Optional[int] = None,
        affinity: Optional[Dict[str, Any]] = None,
        automount_service_account_token: Optional[bool] = None,
        containers: Optional[Dict[str, Any]] = None,
        dns_config: Optional[Dict[str, Any]] = None,
        dns_policy: Optional[str] = "",
        enable_service_links: Optional[bool] = None,
        ephemeral_containers: Optional[Dict[str, Any]] = None,
        host_aliases: Optional[Dict[str, Any]] = None,
        host_ipc: Optional[bool] = None,
        host_network: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        host_users: Optional[bool] = None,
        hostname: Optional[str] = "",
        image_pull_secrets: Optional[Dict[str, Any]] = None,
        init_containers: Optional[Dict[str, Any]] = None,
        node_name: Optional[str] = "",
        node_selector: Optional[Dict[str, Any]] = None,
        os: Optional[Dict[str, Any]] = None,
        overhead: Optional[Dict[str, Any]] = None,
        preemption_policy: Optional[str] = "",
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = "",
        readiness_gates: Optional[Dict[str, Any]] = None,
        resource_claims: Optional[Dict[str, Any]] = None,
        restart_policy: Optional[str] = "",
        runtime_class_name: Optional[str] = "",
        scheduler_name: Optional[str] = "",
        scheduling_gates: Optional[Dict[str, Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service_account: Optional[str] = "",
        service_account_name: Optional[str] = "",
        set_hostname_as_fqdn: Optional[bool] = None,
        share_process_namespace: Optional[bool] = None,
        subdomain: Optional[str] = "",
        termination_grace_period_seconds: Optional[int] = None,
        tolerations: Optional[Dict[str, Any]] = None,
        topology_spread_constraints: Optional[Dict[str, Any]] = None,
        volumes: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            active_deadline_seconds(int): Optional duration in seconds the pod may be active on the node relative to
              StartTime before the system will actively try to mark it failed and kill
              associated containers. Value must be a positive integer.

            affinity(Dict[Any, Any]): If specified, the pod's scheduling constraints
              Affinity is a group of affinity scheduling rules.

              FIELDS:
                nodeAffinity	<NodeAffinity>
                  Describes node affinity scheduling rules for the pod.

                podAffinity	<PodAffinity>
                  Describes pod affinity scheduling rules (e.g. co-locate this pod in the same
                  node, zone, etc. as some other pod(s)).

                podAntiAffinity	<PodAntiAffinity>
                  Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in
                  the same node, zone, etc. as some other pod(s)).

            automount_service_account_token(bool): AutomountServiceAccountToken indicates whether a service account token
              should be automatically mounted.

            containers(Dict[Any, Any]): List of containers belonging to the pod. Containers cannot currently be
              added or removed. There must be at least one container in a Pod. Cannot be
              updated.
              A single application container that you want to run within a pod.

              FIELDS:
                args	<[]string>
                  Arguments to the entrypoint. The container image's CMD is used if this is
                  not provided. Variable references $(VAR_NAME) are expanded using the
                  container's environment. If a variable cannot be resolved, the reference in
                  the input string will be unchanged. Double $$ are reduced to a single $,
                  which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will
                  produce the string literal "$(VAR_NAME)". Escaped references will never be
                  expanded, regardless of whether the variable exists or not. Cannot be
                  updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                command	<[]string>
                  Entrypoint array. Not executed within a shell. The container image's
                  ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME)
                  are expanded using the container's environment. If a variable cannot be
                  resolved, the reference in the input string will be unchanged. Double $$ are
                  reduced to a single $, which allows for escaping the $(VAR_NAME) syntax:
                  i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped
                  references will never be expanded, regardless of whether the variable exists
                  or not. Cannot be updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                env	<[]EnvVar>
                  List of environment variables to set in the container. Cannot be updated.

                envFrom	<[]EnvFromSource>
                  List of sources to populate environment variables in the container. The keys
                  defined within a source must be a C_IDENTIFIER. All invalid keys will be
                  reported as an event when the container is starting. When a key exists in
                  multiple sources, the value associated with the last source will take
                  precedence. Values defined by an Env with a duplicate key will take
                  precedence. Cannot be updated.

                image	<string>
                  Container image name. More info:
                  https://kubernetes.io/docs/concepts/containers/images This field is optional
                  to allow higher level config management to default or override container
                  images in workload controllers like Deployments and StatefulSets.

                imagePullPolicy	<string>
                  Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if
                  :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More
                  info: https://kubernetes.io/docs/concepts/containers/images#updating-images

                  Possible enum values:
                   - `"Always"` means that kubelet always attempts to pull the latest image.
                  Container will fail If the pull fails.
                   - `"IfNotPresent"` means that kubelet pulls if the image isn't present on
                  disk. Container will fail if the image isn't present and the pull fails.
                   - `"Never"` means that kubelet never pulls an image, but only uses a local
                  image. Container will fail if the image isn't present

                lifecycle	<Lifecycle>
                  Actions that the management system should take in response to container
                  lifecycle events. Cannot be updated.

                livenessProbe	<Probe>
                  Periodic probe of container liveness. Container will be restarted if the
                  probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                name	<string> -required-
                  Name of the container specified as a DNS_LABEL. Each container in a pod must
                  have a unique name (DNS_LABEL). Cannot be updated.

                ports	<[]ContainerPort>
                  List of ports to expose from the container. Not specifying a port here DOES
                  NOT prevent that port from being exposed. Any port which is listening on the
                  default "0.0.0.0" address inside a container will be accessible from the
                  network. Modifying this array with strategic merge patch may corrupt the
                  data. For more information See
                  https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated.

                readinessProbe	<Probe>
                  Periodic probe of container service readiness. Container will be removed
                  from service endpoints if the probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                resizePolicy	<[]ContainerResizePolicy>
                  Resources resize policy for the container.

                resources	<ResourceRequirements>
                  Compute Resources required by this container. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                restartPolicy	<string>
                  RestartPolicy defines the restart behavior of individual containers in a
                  pod. This field may only be set for init containers, and the only allowed
                  value is "Always". For non-init containers or when this field is not
                  specified, the restart behavior is defined by the Pod's restart policy and
                  the container type. Setting the RestartPolicy as "Always" for the init
                  container will have the following effect: this init container will be
                  continually restarted on exit until all regular containers have terminated.
                  Once all regular containers have completed, all init containers with
                  restartPolicy "Always" will be shut down. This lifecycle differs from normal
                  init containers and is often referred to as a "sidecar" container. Although
                  this init container still starts in the init container sequence, it does not
                  wait for the container to complete before proceeding to the next init
                  container. Instead, the next init container starts immediately after this
                  init container is started, or after any startupProbe has successfully
                  completed.

                securityContext	<SecurityContext>
                  SecurityContext defines the security options the container should be run
                  with. If set, the fields of SecurityContext override the equivalent fields
                  of PodSecurityContext. More info:
                  https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

                startupProbe	<Probe>
                  StartupProbe indicates that the Pod has successfully initialized. If
                  specified, no other probes are executed until this completes successfully.
                  If this probe fails, the Pod will be restarted, just as if the livenessProbe
                  failed. This can be used to provide different probe parameters at the
                  beginning of a Pod's lifecycle, when it might take a long time to load data
                  or warm a cache, than during steady-state operation. This cannot be updated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                stdin	<boolean>
                  Whether this container should allocate a buffer for stdin in the container
                  runtime. If this is not set, reads from stdin in the container will always
                  result in EOF. Default is false.

                stdinOnce	<boolean>
                  Whether the container runtime should close the stdin channel after it has
                  been opened by a single attach. When stdin is true the stdin stream will
                  remain open across multiple attach sessions. If stdinOnce is set to true,
                  stdin is opened on container start, is empty until the first client attaches
                  to stdin, and then remains open and accepts data until the client
                  disconnects, at which time stdin is closed and remains closed until the
                  container is restarted. If this flag is false, a container processes that
                  reads from stdin will never receive an EOF. Default is false

                terminationMessagePath	<string>
                  Optional: Path at which the file to which the container's termination
                  message will be written is mounted into the container's filesystem. Message
                  written is intended to be brief final status, such as an assertion failure
                  message. Will be truncated by the node if greater than 4096 bytes. The total
                  message length across all containers will be limited to 12kb. Defaults to
                  /dev/termination-log. Cannot be updated.

                terminationMessagePolicy	<string>
                  Indicate how the termination message should be populated. File will use the
                  contents of terminationMessagePath to populate the container status message
                  on both success and failure. FallbackToLogsOnError will use the last chunk
                  of container log output if the termination message file is empty and the
                  container exited with an error. The log output is limited to 2048 bytes or
                  80 lines, whichever is smaller. Defaults to File. Cannot be updated.

                  Possible enum values:
                   - `"FallbackToLogsOnError"` will read the most recent contents of the
                  container logs for the container status message when the container exits
                  with an error and the terminationMessagePath has no contents.
                   - `"File"` is the default behavior and will set the container status
                  message to the contents of the container's terminationMessagePath when the
                  container exits.

                tty	<boolean>
                  Whether this container should allocate a TTY for itself, also requires
                  'stdin' to be true. Default is false.

                volumeDevices	<[]VolumeDevice>
                  volumeDevices is the list of block devices to be used by the container.

                volumeMounts	<[]VolumeMount>
                  Pod volumes to mount into the container's filesystem. Cannot be updated.

                workingDir	<string>
                  Container's working directory. If not specified, the container runtime's
                  default will be used, which might be configured in the container image.
                  Cannot be updated.

            dns_config(Dict[Any, Any]): Specifies the DNS parameters of a pod. Parameters specified here will be
              merged to the generated DNS configuration based on DNSPolicy.
              PodDNSConfig defines the DNS parameters of a pod in addition to those
              generated from DNSPolicy.

              FIELDS:
                nameservers	<[]string>
                  A list of DNS name server IP addresses. This will be appended to the base
                  nameservers generated from DNSPolicy. Duplicated nameservers will be
                  removed.

                options	<[]PodDNSConfigOption>
                  A list of DNS resolver options. This will be merged with the base options
                  generated from DNSPolicy. Duplicated entries will be removed. Resolution
                  options given in Options will override those that appear in the base
                  DNSPolicy.

                searches	<[]string>
                  A list of DNS search domains for host-name lookup. This will be appended to
                  the base search paths generated from DNSPolicy. Duplicated search paths will
                  be removed.

            dns_policy(str): Set DNS policy for the pod. Defaults to "ClusterFirst". Valid values are
              'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS
              parameters given in DNSConfig will be merged with the policy selected with
              DNSPolicy. To have DNS options set along with hostNetwork, you have to
              specify DNS policy explicitly to 'ClusterFirstWithHostNet'.

              Possible enum values:
               - `"ClusterFirst"` indicates that the pod should use cluster DNS first
              unless hostNetwork is true, if it is available, then fall back on the
              default (as determined by kubelet) DNS settings.
               - `"ClusterFirstWithHostNet"` indicates that the pod should use cluster DNS
              first, if it is available, then fall back on the default (as determined by
              kubelet) DNS settings.
               - `"Default"` indicates that the pod should use the default (as determined
              by kubelet) DNS settings.
               - `"None"` indicates that the pod should use empty DNS settings. DNS
              parameters such as nameservers and search paths should be defined via
              DNSConfig.

            enable_service_links(bool): EnableServiceLinks indicates whether information about services should be
              injected into pod's environment variables, matching the syntax of Docker
              links. Optional: Defaults to true.

            ephemeral_containers(Dict[Any, Any]): List of ephemeral containers run in this pod. Ephemeral containers may be
              run in an existing pod to perform user-initiated actions such as debugging.
              This list cannot be specified when creating a pod, and it cannot be modified
              by updating the pod spec. In order to add an ephemeral container to an
              existing pod, use the pod's ephemeralcontainers subresource.
              An EphemeralContainer is a temporary container that you may add to an
              existing Pod for user-initiated activities such as debugging. Ephemeral
              containers have no resource or scheduling guarantees, and they will not be
              restarted when they exit or when a Pod is removed or restarted. The kubelet
              may evict a Pod if an ephemeral container causes the Pod to exceed its
              resource allocation.

              To add an ephemeral container, use the ephemeralcontainers subresource of an
              existing Pod. Ephemeral containers may not be removed or restarted.

              FIELDS:
                args	<[]string>
                  Arguments to the entrypoint. The image's CMD is used if this is not
                  provided. Variable references $(VAR_NAME) are expanded using the container's
                  environment. If a variable cannot be resolved, the reference in the input
                  string will be unchanged. Double $$ are reduced to a single $, which allows
                  for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the
                  string literal "$(VAR_NAME)". Escaped references will never be expanded,
                  regardless of whether the variable exists or not. Cannot be updated. More
                  info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                command	<[]string>
                  Entrypoint array. Not executed within a shell. The image's ENTRYPOINT is
                  used if this is not provided. Variable references $(VAR_NAME) are expanded
                  using the container's environment. If a variable cannot be resolved, the
                  reference in the input string will be unchanged. Double $$ are reduced to a
                  single $, which allows for escaping the $(VAR_NAME) syntax: i.e.
                  "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped
                  references will never be expanded, regardless of whether the variable exists
                  or not. Cannot be updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                env	<[]EnvVar>
                  List of environment variables to set in the container. Cannot be updated.

                envFrom	<[]EnvFromSource>
                  List of sources to populate environment variables in the container. The keys
                  defined within a source must be a C_IDENTIFIER. All invalid keys will be
                  reported as an event when the container is starting. When a key exists in
                  multiple sources, the value associated with the last source will take
                  precedence. Values defined by an Env with a duplicate key will take
                  precedence. Cannot be updated.

                image	<string>
                  Container image name. More info:
                  https://kubernetes.io/docs/concepts/containers/images

                imagePullPolicy	<string>
                  Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if
                  :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More
                  info: https://kubernetes.io/docs/concepts/containers/images#updating-images

                  Possible enum values:
                   - `"Always"` means that kubelet always attempts to pull the latest image.
                  Container will fail If the pull fails.
                   - `"IfNotPresent"` means that kubelet pulls if the image isn't present on
                  disk. Container will fail if the image isn't present and the pull fails.
                   - `"Never"` means that kubelet never pulls an image, but only uses a local
                  image. Container will fail if the image isn't present

                lifecycle	<Lifecycle>
                  Lifecycle is not allowed for ephemeral containers.

                livenessProbe	<Probe>
                  Probes are not allowed for ephemeral containers.

                name	<string> -required-
                  Name of the ephemeral container specified as a DNS_LABEL. This name must be
                  unique among all containers, init containers and ephemeral containers.

                ports	<[]ContainerPort>
                  Ports are not allowed for ephemeral containers.

                readinessProbe	<Probe>
                  Probes are not allowed for ephemeral containers.

                resizePolicy	<[]ContainerResizePolicy>
                  Resources resize policy for the container.

                resources	<ResourceRequirements>
                  Resources are not allowed for ephemeral containers. Ephemeral containers use
                  spare resources already allocated to the pod.

                restartPolicy	<string>
                  Restart policy for the container to manage the restart behavior of each
                  container within a pod. This may only be set for init containers. You cannot
                  set this field on ephemeral containers.

                securityContext	<SecurityContext>
                  Optional: SecurityContext defines the security options the ephemeral
                  container should be run with. If set, the fields of SecurityContext override
                  the equivalent fields of PodSecurityContext.

                startupProbe	<Probe>
                  Probes are not allowed for ephemeral containers.

                stdin	<boolean>
                  Whether this container should allocate a buffer for stdin in the container
                  runtime. If this is not set, reads from stdin in the container will always
                  result in EOF. Default is false.

                stdinOnce	<boolean>
                  Whether the container runtime should close the stdin channel after it has
                  been opened by a single attach. When stdin is true the stdin stream will
                  remain open across multiple attach sessions. If stdinOnce is set to true,
                  stdin is opened on container start, is empty until the first client attaches
                  to stdin, and then remains open and accepts data until the client
                  disconnects, at which time stdin is closed and remains closed until the
                  container is restarted. If this flag is false, a container processes that
                  reads from stdin will never receive an EOF. Default is false

                targetContainerName	<string>
                  If set, the name of the container from PodSpec that this ephemeral container
                  targets. The ephemeral container will be run in the namespaces (IPC, PID,
                  etc) of this container. If not set then the ephemeral container uses the
                  namespaces configured in the Pod spec.

                  The container runtime must implement support for this feature. If the
                  runtime does not support namespace targeting then the result of setting this
                  field is undefined.

                terminationMessagePath	<string>
                  Optional: Path at which the file to which the container's termination
                  message will be written is mounted into the container's filesystem. Message
                  written is intended to be brief final status, such as an assertion failure
                  message. Will be truncated by the node if greater than 4096 bytes. The total
                  message length across all containers will be limited to 12kb. Defaults to
                  /dev/termination-log. Cannot be updated.

                terminationMessagePolicy	<string>
                  Indicate how the termination message should be populated. File will use the
                  contents of terminationMessagePath to populate the container status message
                  on both success and failure. FallbackToLogsOnError will use the last chunk
                  of container log output if the termination message file is empty and the
                  container exited with an error. The log output is limited to 2048 bytes or
                  80 lines, whichever is smaller. Defaults to File. Cannot be updated.

                  Possible enum values:
                   - `"FallbackToLogsOnError"` will read the most recent contents of the
                  container logs for the container status message when the container exits
                  with an error and the terminationMessagePath has no contents.
                   - `"File"` is the default behavior and will set the container status
                  message to the contents of the container's terminationMessagePath when the
                  container exits.

                tty	<boolean>
                  Whether this container should allocate a TTY for itself, also requires
                  'stdin' to be true. Default is false.

                volumeDevices	<[]VolumeDevice>
                  volumeDevices is the list of block devices to be used by the container.

                volumeMounts	<[]VolumeMount>
                  Pod volumes to mount into the container's filesystem. Subpath mounts are not
                  allowed for ephemeral containers. Cannot be updated.

                workingDir	<string>
                  Container's working directory. If not specified, the container runtime's
                  default will be used, which might be configured in the container image.
                  Cannot be updated.

            host_aliases(Dict[Any, Any]): HostAliases is an optional list of hosts and IPs that will be injected into
              the pod's hosts file if specified.
              HostAlias holds the mapping between IP and hostnames that will be injected
              as an entry in the pod's hosts file.

              FIELDS:
                hostnames	<[]string>
                  Hostnames for the above IP address.

                ip	<string> -required-
                  IP address of the host file entry.

            host_ipc(bool): Use the host's ipc namespace. Optional: Default to false.

            host_network(bool): Host networking requested for this pod. Use the host's network namespace. If
              this option is set, the ports that will be used must be specified. Default
              to false.

            host_pid(bool): Use the host's pid namespace. Optional: Default to false.

            host_users(bool): Use the host's user namespace. Optional: Default to true. If set to true or
              not present, the pod will be run in the host user namespace, useful for when
              the pod needs a feature only available to the host user namespace, such as
              loading a kernel module with CAP_SYS_MODULE. When set to false, a new userns
              is created for the pod. Setting false is useful for mitigating container
              breakout vulnerabilities even allowing users to run their containers as root
              without actually having root privileges on the host. This field is
              alpha-level and is only honored by servers that enable the
              UserNamespacesSupport feature.

            hostname(str): Specifies the hostname of the Pod If not specified, the pod's hostname will
              be set to a system-defined value.

            image_pull_secrets(Dict[Any, Any]): ImagePullSecrets is an optional list of references to secrets in the same
              namespace to use for pulling any of the images used by this PodSpec. If
              specified, these secrets will be passed to individual puller implementations
              for them to use. More info:
              https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod
              LocalObjectReference contains enough information to let you locate the
              referenced object inside the same namespace.

              FIELDS:
                name	<string>
                  Name of the referent. This field is effectively required, but due to
                  backwards compatibility is allowed to be empty. Instances of this type with
                  an empty value here are almost certainly wrong. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

            init_containers(Dict[Any, Any]): List of initialization containers belonging to the pod. Init containers are
              executed in order prior to containers being started. If any init container
              fails, the pod is considered to have failed and is handled according to its
              restartPolicy. The name for an init container or normal container must be
              unique among all containers. Init containers may not have Lifecycle actions,
              Readiness probes, Liveness probes, or Startup probes. The
              resourceRequirements of an init container are taken into account during
              scheduling by finding the highest request/limit for each resource type, and
              then using the max of of that value or the sum of the normal containers.
              Limits are applied to init containers in a similar fashion. Init containers
              cannot currently be added or removed. Cannot be updated. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
              A single application container that you want to run within a pod.

              FIELDS:
                args	<[]string>
                  Arguments to the entrypoint. The container image's CMD is used if this is
                  not provided. Variable references $(VAR_NAME) are expanded using the
                  container's environment. If a variable cannot be resolved, the reference in
                  the input string will be unchanged. Double $$ are reduced to a single $,
                  which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will
                  produce the string literal "$(VAR_NAME)". Escaped references will never be
                  expanded, regardless of whether the variable exists or not. Cannot be
                  updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                command	<[]string>
                  Entrypoint array. Not executed within a shell. The container image's
                  ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME)
                  are expanded using the container's environment. If a variable cannot be
                  resolved, the reference in the input string will be unchanged. Double $$ are
                  reduced to a single $, which allows for escaping the $(VAR_NAME) syntax:
                  i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped
                  references will never be expanded, regardless of whether the variable exists
                  or not. Cannot be updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                env	<[]EnvVar>
                  List of environment variables to set in the container. Cannot be updated.

                envFrom	<[]EnvFromSource>
                  List of sources to populate environment variables in the container. The keys
                  defined within a source must be a C_IDENTIFIER. All invalid keys will be
                  reported as an event when the container is starting. When a key exists in
                  multiple sources, the value associated with the last source will take
                  precedence. Values defined by an Env with a duplicate key will take
                  precedence. Cannot be updated.

                image	<string>
                  Container image name. More info:
                  https://kubernetes.io/docs/concepts/containers/images This field is optional
                  to allow higher level config management to default or override container
                  images in workload controllers like Deployments and StatefulSets.

                imagePullPolicy	<string>
                  Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if
                  :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More
                  info: https://kubernetes.io/docs/concepts/containers/images#updating-images

                  Possible enum values:
                   - `"Always"` means that kubelet always attempts to pull the latest image.
                  Container will fail If the pull fails.
                   - `"IfNotPresent"` means that kubelet pulls if the image isn't present on
                  disk. Container will fail if the image isn't present and the pull fails.
                   - `"Never"` means that kubelet never pulls an image, but only uses a local
                  image. Container will fail if the image isn't present

                lifecycle	<Lifecycle>
                  Actions that the management system should take in response to container
                  lifecycle events. Cannot be updated.

                livenessProbe	<Probe>
                  Periodic probe of container liveness. Container will be restarted if the
                  probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                name	<string> -required-
                  Name of the container specified as a DNS_LABEL. Each container in a pod must
                  have a unique name (DNS_LABEL). Cannot be updated.

                ports	<[]ContainerPort>
                  List of ports to expose from the container. Not specifying a port here DOES
                  NOT prevent that port from being exposed. Any port which is listening on the
                  default "0.0.0.0" address inside a container will be accessible from the
                  network. Modifying this array with strategic merge patch may corrupt the
                  data. For more information See
                  https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated.

                readinessProbe	<Probe>
                  Periodic probe of container service readiness. Container will be removed
                  from service endpoints if the probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                resizePolicy	<[]ContainerResizePolicy>
                  Resources resize policy for the container.

                resources	<ResourceRequirements>
                  Compute Resources required by this container. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                restartPolicy	<string>
                  RestartPolicy defines the restart behavior of individual containers in a
                  pod. This field may only be set for init containers, and the only allowed
                  value is "Always". For non-init containers or when this field is not
                  specified, the restart behavior is defined by the Pod's restart policy and
                  the container type. Setting the RestartPolicy as "Always" for the init
                  container will have the following effect: this init container will be
                  continually restarted on exit until all regular containers have terminated.
                  Once all regular containers have completed, all init containers with
                  restartPolicy "Always" will be shut down. This lifecycle differs from normal
                  init containers and is often referred to as a "sidecar" container. Although
                  this init container still starts in the init container sequence, it does not
                  wait for the container to complete before proceeding to the next init
                  container. Instead, the next init container starts immediately after this
                  init container is started, or after any startupProbe has successfully
                  completed.

                securityContext	<SecurityContext>
                  SecurityContext defines the security options the container should be run
                  with. If set, the fields of SecurityContext override the equivalent fields
                  of PodSecurityContext. More info:
                  https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

                startupProbe	<Probe>
                  StartupProbe indicates that the Pod has successfully initialized. If
                  specified, no other probes are executed until this completes successfully.
                  If this probe fails, the Pod will be restarted, just as if the livenessProbe
                  failed. This can be used to provide different probe parameters at the
                  beginning of a Pod's lifecycle, when it might take a long time to load data
                  or warm a cache, than during steady-state operation. This cannot be updated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                stdin	<boolean>
                  Whether this container should allocate a buffer for stdin in the container
                  runtime. If this is not set, reads from stdin in the container will always
                  result in EOF. Default is false.

                stdinOnce	<boolean>
                  Whether the container runtime should close the stdin channel after it has
                  been opened by a single attach. When stdin is true the stdin stream will
                  remain open across multiple attach sessions. If stdinOnce is set to true,
                  stdin is opened on container start, is empty until the first client attaches
                  to stdin, and then remains open and accepts data until the client
                  disconnects, at which time stdin is closed and remains closed until the
                  container is restarted. If this flag is false, a container processes that
                  reads from stdin will never receive an EOF. Default is false

                terminationMessagePath	<string>
                  Optional: Path at which the file to which the container's termination
                  message will be written is mounted into the container's filesystem. Message
                  written is intended to be brief final status, such as an assertion failure
                  message. Will be truncated by the node if greater than 4096 bytes. The total
                  message length across all containers will be limited to 12kb. Defaults to
                  /dev/termination-log. Cannot be updated.

                terminationMessagePolicy	<string>
                  Indicate how the termination message should be populated. File will use the
                  contents of terminationMessagePath to populate the container status message
                  on both success and failure. FallbackToLogsOnError will use the last chunk
                  of container log output if the termination message file is empty and the
                  container exited with an error. The log output is limited to 2048 bytes or
                  80 lines, whichever is smaller. Defaults to File. Cannot be updated.

                  Possible enum values:
                   - `"FallbackToLogsOnError"` will read the most recent contents of the
                  container logs for the container status message when the container exits
                  with an error and the terminationMessagePath has no contents.
                   - `"File"` is the default behavior and will set the container status
                  message to the contents of the container's terminationMessagePath when the
                  container exits.

                tty	<boolean>
                  Whether this container should allocate a TTY for itself, also requires
                  'stdin' to be true. Default is false.

                volumeDevices	<[]VolumeDevice>
                  volumeDevices is the list of block devices to be used by the container.

                volumeMounts	<[]VolumeMount>
                  Pod volumes to mount into the container's filesystem. Cannot be updated.

                workingDir	<string>
                  Container's working directory. If not specified, the container runtime's
                  default will be used, which might be configured in the container image.
                  Cannot be updated.

            node_name(str): NodeName is a request to schedule this pod onto a specific node. If it is
              non-empty, the scheduler simply schedules this pod onto that node, assuming
              that it fits resource requirements.

            node_selector(Dict[Any, Any]): NodeSelector is a selector which must be true for the pod to fit on a node.
              Selector which must match a node's labels for the pod to be scheduled on
              that node. More info:
              https://kubernetes.io/docs/concepts/configuration/assign-pod-node/

            os(Dict[Any, Any]): Specifies the OS of the containers in the pod. Some pod and container fields
              are restricted if this is set.

              If the OS field is set to linux, the following fields must be unset:
              -securityContext.windowsOptions

              If the OS field is set to windows, following fields must be unset: -
              spec.hostPID - spec.hostIPC - spec.hostUsers -
              spec.securityContext.appArmorProfile - spec.securityContext.seLinuxOptions -
              spec.securityContext.seccompProfile - spec.securityContext.fsGroup -
              spec.securityContext.fsGroupChangePolicy - spec.securityContext.sysctls -
              spec.shareProcessNamespace - spec.securityContext.runAsUser -
              spec.securityContext.runAsGroup - spec.securityContext.supplementalGroups -
              spec.containers[*].securityContext.appArmorProfile -
              spec.containers[*].securityContext.seLinuxOptions -
              spec.containers[*].securityContext.seccompProfile -
              spec.containers[*].securityContext.capabilities -
              spec.containers[*].securityContext.readOnlyRootFilesystem -
              spec.containers[*].securityContext.privileged -
              spec.containers[*].securityContext.allowPrivilegeEscalation -
              spec.containers[*].securityContext.procMount -
              spec.containers[*].securityContext.runAsUser -
              spec.containers[*].securityContext.runAsGroup
              PodOS defines the OS parameters of a pod.

              FIELDS:
                name	<string> -required-
                  Name is the name of the operating system. The currently supported values are
                  linux and windows. Additional value may be defined in future and can be one
                  of:
                  https://github.com/opencontainers/runtime-spec/blob/master/config.md#platform-specific-configuration
                  Clients should expect to handle additional values and treat unrecognized
                  values in this field as os: null

            overhead(Dict[Any, Any]): Overhead represents the resource overhead associated with running a pod for
              a given RuntimeClass. This field will be autopopulated at admission time by
              the RuntimeClass admission controller. If the RuntimeClass admission
              controller is enabled, overhead must not be set in Pod create requests. The
              RuntimeClass admission controller will reject Pod create requests which have
              the overhead already set. If RuntimeClass is configured and selected in the
              PodSpec, Overhead will be set to the value defined in the corresponding
              RuntimeClass, otherwise it will remain unset and treated as zero. More info:
              https://git.k8s.io/enhancements/keps/sig-node/688-pod-overhead/README.md
              Quantity is a fixed-point representation of a number. It provides convenient
              marshaling/unmarshaling in JSON and YAML, in addition to String() and
              AsInt64() accessors.

              The serialization format is:

              ``` <quantity>        ::= <signedNumber><suffix>

                (Note that <suffix> may be empty, from the "" case in <decimalSI>.)

              <digit>           ::= 0 | 1 | ... | 9 <digits>          ::= <digit> |
              <digit><digits> <number>          ::= <digits> | <digits>.<digits> |
              <digits>. | .<digits> <sign>            ::= "+" | "-" <signedNumber>    ::=
              <number> | <sign><number> <suffix>          ::= <binarySI> |
              <decimalExponent> | <decimalSI> <binarySI>        ::= Ki | Mi | Gi | Ti | Pi
              | Ei

                (International System of units; See:
              http://physics.nist.gov/cuu/Units/binary.html)

              <decimalSI>       ::= m | "" | k | M | G | T | P | E

                (Note that 1024 = 1Ki but 1000 = 1k; I didn't choose the capitalization.)

              <decimalExponent> ::= "e" <signedNumber> | "E" <signedNumber> ```

              No matter which of the three exponent forms is used, no quantity may
              represent a number greater than 2^63-1 in magnitude, nor may it have more
              than 3 decimal places. Numbers larger or more precise will be capped or
              rounded up. (E.g.: 0.1m will rounded up to 1m.) This may be extended in the
              future if we require larger or smaller quantities.

              When a Quantity is parsed from a string, it will remember the type of suffix
              it had, and will use the same type again when it is serialized.

              Before serializing, Quantity will be put in "canonical form". This means
              that Exponent/suffix will be adjusted up or down (with a corresponding
              increase or decrease in Mantissa) such that:

              - No precision is lost - No fractional digits will be emitted - The exponent
              (or suffix) is as large as possible.

              The sign will be omitted unless the number is negative.

              Examples:

              - 1.5 will be serialized as "1500m" - 1.5Gi will be serialized as "1536Mi"

              Note that the quantity will NEVER be internally represented by a floating
              point number. That is the whole point of this exercise.

              Non-canonical values will still parse as long as they are well formed, but
              will be re-emitted in their canonical form. (So always use canonical form,
              or don't diff.)

              This format is intended to make it difficult to use these numbers without
              writing some sort of special handling code in the hopes that that will cause
              implementors to also use a fixed point implementation.

            preemption_policy(str): PreemptionPolicy is the Policy for preempting pods with lower priority. One
              of Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if unset.

              Possible enum values:
               - `"Never"` means that pod never preempts other pods with lower priority.
               - `"PreemptLowerPriority"` means that pod can preempt other pods with lower
              priority.

            priority(int): The priority value. Various system components use this field to find the
              priority of the pod. When Priority Admission Controller is enabled, it
              prevents users from setting this field. The admission controller populates
              this field from PriorityClassName. The higher the value, the higher the
              priority.

            priority_class_name(str): If specified, indicates the pod's priority. "system-node-critical" and
              "system-cluster-critical" are two special keywords which indicate the
              highest priorities with the former being the highest priority. Any other
              name must be defined by creating a PriorityClass object with that name. If
              not specified, the pod priority will be default or zero if there is no
              default.

            readiness_gates(Dict[Any, Any]): If specified, all readiness gates will be evaluated for pod readiness. A pod
              is ready when all its containers are ready AND all conditions specified in
              the readiness gates have status equal to "True" More info:
              https://git.k8s.io/enhancements/keps/sig-network/580-pod-readiness-gates
              PodReadinessGate contains the reference to a pod condition

              FIELDS:
                conditionType	<string> -required-
                  ConditionType refers to a condition in the pod's condition list with
                  matching type.

            resource_claims(Dict[Any, Any]): ResourceClaims defines which ResourceClaims must be allocated and reserved
              before the Pod is allowed to start. The resources will be made available to
              those containers which consume them by name.

              This is an alpha field and requires enabling the DynamicResourceAllocation
              feature gate.

              This field is immutable.
              PodResourceClaim references exactly one ResourceClaim through a ClaimSource.
              It adds a name to it that uniquely identifies the ResourceClaim inside the
              Pod. Containers that need access to the ResourceClaim reference it with this
              name.

              FIELDS:
                name	<string> -required-
                  Name uniquely identifies this resource claim inside the pod. This must be a
                  DNS_LABEL.

                source	<ClaimSource>
                  Source describes where to find the ResourceClaim.

            restart_policy(str): Restart policy for all containers within the pod. One of Always, OnFailure,
              Never. In some contexts, only a subset of those values may be permitted.
              Default to Always. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy

              Possible enum values:
               - `"Always"`
               - `"Never"`
               - `"OnFailure"`

            runtime_class_name(str): RuntimeClassName refers to a RuntimeClass object in the node.k8s.io group,
              which should be used to run this pod.  If no RuntimeClass resource matches
              the named class, the pod will not be run. If unset or empty, the "legacy"
              RuntimeClass will be used, which is an implicit class with an empty
              definition that uses the default runtime handler. More info:
              https://git.k8s.io/enhancements/keps/sig-node/585-runtime-class

            scheduler_name(str): If specified, the pod will be dispatched by specified scheduler. If not
              specified, the pod will be dispatched by default scheduler.

            scheduling_gates(Dict[Any, Any]): SchedulingGates is an opaque list of values that if specified will block
              scheduling the pod. If schedulingGates is not empty, the pod will stay in
              the SchedulingGated state and the scheduler will not attempt to schedule the
              pod.

              SchedulingGates can only be set at pod creation time, and be removed only
              afterwards.
              PodSchedulingGate is associated to a Pod to guard its scheduling.

              FIELDS:
                name	<string> -required-
                  Name of the scheduling gate. Each scheduling gate must have a unique name
                  field.

            security_context(Dict[Any, Any]): SecurityContext holds pod-level security attributes and common container
              settings. Optional: Defaults to empty.  See type description for default
              values of each field.
              PodSecurityContext holds pod-level security attributes and common container
              settings. Some fields are also present in container.securityContext.  Field
              values of container.securityContext take precedence over field values of
              PodSecurityContext.

              FIELDS:
                appArmorProfile	<AppArmorProfile>
                  appArmorProfile is the AppArmor options to use by the containers in this
                  pod. Note that this field cannot be set when spec.os.name is windows.

                fsGroup	<integer>
                  A special supplemental group that applies to all containers in a pod. Some
                  volume types allow the Kubelet to change the ownership of that volume to be
                  owned by the pod:

                  1. The owning GID will be the FSGroup 2. The setgid bit is set (new files
                  created in the volume will be owned by FSGroup) 3. The permission bits are
                  OR'd with rw-rw----

                  If unset, the Kubelet will not modify the ownership and permissions of any
                  volume. Note that this field cannot be set when spec.os.name is windows.

                fsGroupChangePolicy	<string>
                  fsGroupChangePolicy defines behavior of changing ownership and permission of
                  the volume before being exposed inside Pod. This field will only apply to
                  volume types which support fsGroup based ownership(and permissions). It will
                  have no effect on ephemeral volume types such as: secret, configmaps and
                  emptydir. Valid values are "OnRootMismatch" and "Always". If not specified,
                  "Always" is used. Note that this field cannot be set when spec.os.name is
                  windows.

                  Possible enum values:
                   - `"Always"` indicates that volume's ownership and permissions should
                  always be changed whenever volume is mounted inside a Pod. This the default
                  behavior.
                   - `"OnRootMismatch"` indicates that volume's ownership and permissions will
                  be changed only when permission and ownership of root directory does not
                  match with expected permissions on the volume. This can help shorten the
                  time it takes to change ownership and permissions of a volume.

                runAsGroup	<integer>
                  The GID to run the entrypoint of the container process. Uses runtime default
                  if unset. May also be set in SecurityContext.  If set in both
                  SecurityContext and PodSecurityContext, the value specified in
                  SecurityContext takes precedence for that container. Note that this field
                  cannot be set when spec.os.name is windows.

                runAsNonRoot	<boolean>
                  Indicates that the container must run as a non-root user. If true, the
                  Kubelet will validate the image at runtime to ensure that it does not run as
                  UID 0 (root) and fail to start the container if it does. If unset or false,
                  no such validation will be performed. May also be set in SecurityContext.
                  If set in both SecurityContext and PodSecurityContext, the value specified
                  in SecurityContext takes precedence.

                runAsUser	<integer>
                  The UID to run the entrypoint of the container process. Defaults to user
                  specified in image metadata if unspecified. May also be set in
                  SecurityContext.  If set in both SecurityContext and PodSecurityContext, the
                  value specified in SecurityContext takes precedence for that container. Note
                  that this field cannot be set when spec.os.name is windows.

                seLinuxOptions	<SELinuxOptions>
                  The SELinux context to be applied to all containers. If unspecified, the
                  container runtime will allocate a random SELinux context for each container.
                  May also be set in SecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence
                  for that container. Note that this field cannot be set when spec.os.name is
                  windows.

                seccompProfile	<SeccompProfile>
                  The seccomp options to use by the containers in this pod. Note that this
                  field cannot be set when spec.os.name is windows.

                supplementalGroups	<[]integer>
                  A list of groups applied to the first process run in each container, in
                  addition to the container's primary GID, the fsGroup (if specified), and
                  group memberships defined in the container image for the uid of the
                  container process. If unspecified, no additional groups are added to any
                  container. Note that group memberships defined in the container image for
                  the uid of the container process are still effective, even if they are not
                  included in this list. Note that this field cannot be set when spec.os.name
                  is windows.

                sysctls	<[]Sysctl>
                  Sysctls hold a list of namespaced sysctls used for the pod. Pods with
                  unsupported sysctls (by the container runtime) might fail to launch. Note
                  that this field cannot be set when spec.os.name is windows.

                windowsOptions	<WindowsSecurityContextOptions>
                  The Windows specific settings applied to all containers. If unspecified, the
                  options within a container's SecurityContext will be used. If set in both
                  SecurityContext and PodSecurityContext, the value specified in
                  SecurityContext takes precedence. Note that this field cannot be set when
                  spec.os.name is linux.

            service_account(str): DeprecatedServiceAccount is a deprecated alias for ServiceAccountName.
              Deprecated: Use serviceAccountName instead.

            service_account_name(str): ServiceAccountName is the name of the ServiceAccount to use to run this pod.
              More info:
              https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/

            set_hostname_as_fqdn(bool): If true the pod's hostname will be configured as the pod's FQDN, rather than
              the leaf name (the default). In Linux containers, this means setting the
              FQDN in the hostname field of the kernel (the nodename field of struct
              utsname). In Windows containers, this means setting the registry value of
              hostname for the registry key
              HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters to
              FQDN. If a pod does not have FQDN, this has no effect. Default to false.

            share_process_namespace(bool): Share a single process namespace between all of the containers in a pod.
              When this is set containers will be able to view and signal processes from
              other containers in the same pod, and the first process in each container
              will not be assigned PID 1. HostPID and ShareProcessNamespace cannot both be
              set. Optional: Default to false.

            subdomain(str): If specified, the fully qualified Pod hostname will be
              "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not
              specified, the pod will not have a domainname at all.

            termination_grace_period_seconds(int): Optional duration in seconds the pod needs to terminate gracefully. May be
              decreased in delete request. Value must be non-negative integer. The value
              zero indicates stop immediately via the kill signal (no opportunity to shut
              down). If this value is nil, the default grace period will be used instead.
              The grace period is the duration in seconds after the processes running in
              the pod are sent a termination signal and the time when the processes are
              forcibly halted with a kill signal. Set this value longer than the expected
              cleanup time for your process. Defaults to 30 seconds.

            tolerations(Dict[Any, Any]): If specified, the pod's tolerations.
              The pod this Toleration is attached to tolerates any taint that matches the
              triple <key,value,effect> using the matching operator <operator>.

              FIELDS:
                effect	<string>
                  Effect indicates the taint effect to match. Empty means match all taint
                  effects. When specified, allowed values are NoSchedule, PreferNoSchedule and
                  NoExecute.

                  Possible enum values:
                   - `"NoExecute"` Evict any already-running pods that do not tolerate the
                  taint. Currently enforced by NodeController.
                   - `"NoSchedule"` Do not allow new pods to schedule onto the node unless
                  they tolerate the taint, but allow all pods submitted to Kubelet without
                  going through the scheduler to start, and allow all already-running pods to
                  continue running. Enforced by the scheduler.
                   - `"PreferNoSchedule"` Like TaintEffectNoSchedule, but the scheduler tries
                  not to schedule new pods onto the node, rather than prohibiting new pods
                  from scheduling onto the node entirely. Enforced by the scheduler.

                key	<string>
                  Key is the taint key that the toleration applies to. Empty means match all
                  taint keys. If the key is empty, operator must be Exists; this combination
                  means to match all values and all keys.

                operator	<string>
                  Operator represents a key's relationship to the value. Valid operators are
                  Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for
                  value, so that a pod can tolerate all taints of a particular category.

                  Possible enum values:
                   - `"Equal"`
                   - `"Exists"`

                tolerationSeconds	<integer>
                  TolerationSeconds represents the period of time the toleration (which must
                  be of effect NoExecute, otherwise this field is ignored) tolerates the
                  taint. By default, it is not set, which means tolerate the taint forever (do
                  not evict). Zero and negative values will be treated as 0 (evict
                  immediately) by the system.

                value	<string>
                  Value is the taint value the toleration matches to. If the operator is
                  Exists, the value should be empty, otherwise just a regular string.

            topology_spread_constraints(Dict[Any, Any]): TopologySpreadConstraints describes how a group of pods ought to spread
              across topology domains. Scheduler will schedule pods in a way which abides
              by the constraints. All topologySpreadConstraints are ANDed.
              TopologySpreadConstraint specifies how to spread matching pods among the
              given topology.

              FIELDS:
                labelSelector	<LabelSelector>
                  LabelSelector is used to find matching pods. Pods that match this label
                  selector are counted to determine the number of pods in their corresponding
                  topology domain.

                matchLabelKeys	<[]string>
                  MatchLabelKeys is a set of pod label keys to select the pods over which
                  spreading will be calculated. The keys are used to lookup values from the
                  incoming pod labels, those key-value labels are ANDed with labelSelector to
                  select the group of existing pods over which spreading will be calculated
                  for the incoming pod. The same key is forbidden to exist in both
                  MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when
                  LabelSelector isn't set. Keys that don't exist in the incoming pod labels
                  will be ignored. A null or empty list means only match against
                  labelSelector.

                  This is a beta field and requires the MatchLabelKeysInPodTopologySpread
                  feature gate to be enabled (enabled by default).

                maxSkew	<integer> -required-
                  MaxSkew describes the degree to which pods may be unevenly distributed. When
                  `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference
                  between the number of matching pods in the target topology and the global
                  minimum. The global minimum is the minimum number of matching pods in an
                  eligible domain or zero if the number of eligible domains is less than
                  MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods
                  with the same labelSelector spread as 2/2/1: In this case, the global
                  minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P   | - if
                  MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2;
                  scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on
                  zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be
                  scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used
                  to give higher precedence to topologies that satisfy it. It's a required
                  field. Default value is 1 and 0 is not allowed.

                minDomains	<integer>
                  MinDomains indicates a minimum number of eligible domains. When the number
                  of eligible domains with matching topology keys is less than minDomains, Pod
                  Topology Spread treats "global minimum" as 0, and then the calculation of
                  Skew is performed. And when the number of eligible domains with matching
                  topology keys equals or greater than minDomains, this value has no effect on
                  scheduling. As a result, when the number of eligible domains is less than
                  minDomains, scheduler won't schedule more than maxSkew Pods to those
                  domains. If value is nil, the constraint behaves as if MinDomains is equal
                  to 1. Valid values are integers greater than 0. When value is not nil,
                  WhenUnsatisfiable must be DoNotSchedule.

                  For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to
                  5 and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 |
                  zone3 | |  P P  |  P P  |  P P  | The number of domains is less than
                  5(MinDomains), so "global minimum" is treated as 0. In this situation, new
                  pod with the same labelSelector cannot be scheduled, because computed skew
                  will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will
                  violate MaxSkew.

                nodeAffinityPolicy	<string>
                  NodeAffinityPolicy indicates how we will treat Pod's
                  nodeAffinity/nodeSelector when calculating pod topology spread skew. Options
                  are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in
                  the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes
                  are included in the calculations.

                  If this value is nil, the behavior is equivalent to the Honor policy. This
                  is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                  Possible enum values:
                   - `"Honor"` means use this scheduling directive when calculating pod
                  topology spread skew.
                   - `"Ignore"` means ignore this scheduling directive when calculating pod
                  topology spread skew.

                nodeTaintsPolicy	<string>
                  NodeTaintsPolicy indicates how we will treat node taints when calculating
                  pod topology spread skew. Options are: - Honor: nodes without taints, along
                  with tainted nodes for which the incoming pod has a toleration, are
                  included. - Ignore: node taints are ignored. All nodes are included.

                  If this value is nil, the behavior is equivalent to the Ignore policy. This
                  is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                  Possible enum values:
                   - `"Honor"` means use this scheduling directive when calculating pod
                  topology spread skew.
                   - `"Ignore"` means ignore this scheduling directive when calculating pod
                  topology spread skew.

                topologyKey	<string> -required-
                  TopologyKey is the key of node labels. Nodes that have a label with this key
                  and identical values are considered to be in the same topology. We consider
                  each <key, value> as a "bucket", and try to put balanced number of pods into
                  each bucket. We define a domain as a particular instance of a topology.
                  Also, we define an eligible domain as a domain whose nodes meet the
                  requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey
                  is "kubernetes.io/hostname", each Node is a domain of that topology. And, if
                  TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that
                  topology. It's a required field.

                whenUnsatisfiable	<string> -required-
                  WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the
                  spread constraint. - DoNotSchedule (default) tells the scheduler not to
                  schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any
                  location,
                    but giving higher precedence to topologies that would help reduce the
                    skew.
                  A constraint is considered "Unsatisfiable" for an incoming pod if and only
                  if every possible node assignment for that pod would violate "MaxSkew" on
                  some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and
                  pods with the same labelSelector spread as 3/1/1: | zone1 | zone2 | zone3 |
                  | P P P |   P   |   P   | If WhenUnsatisfiable is set to DoNotSchedule,
                  incoming pod can only be scheduled to zone2(zone3) to become 3/2/1(3/1/2) as
                  ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other words, the
                  cluster can still be imbalanced, but scheduler won't make it *more*
                  imbalanced. It's a required field.

                  Possible enum values:
                   - `"DoNotSchedule"` instructs the scheduler not to schedule the pod when
                  constraints are not satisfied.
                   - `"ScheduleAnyway"` instructs the scheduler to schedule the pod even if
                  constraints are not satisfied.

            volumes(Dict[Any, Any]): List of volumes that can be mounted by containers belonging to the pod. More
              info: https://kubernetes.io/docs/concepts/storage/volumes
              Volume represents a named volume in a pod that may be accessed by any
              container in the pod.

              FIELDS:
                awsElasticBlockStore	<AWSElasticBlockStoreVolumeSource>
                  awsElasticBlockStore represents an AWS Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore

                azureDisk	<AzureDiskVolumeSource>
                  azureDisk represents an Azure Data Disk mount on the host and bind mount to
                  the pod.

                azureFile	<AzureFileVolumeSource>
                  azureFile represents an Azure File Service mount on the host and bind mount
                  to the pod.

                cephfs	<CephFSVolumeSource>
                  cephFS represents a Ceph FS mount on the host that shares a pod's lifetime

                cinder	<CinderVolumeSource>
                  cinder represents a cinder volume attached and mounted on kubelets host
                  machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md

                configMap	<ConfigMapVolumeSource>
                  configMap represents a configMap that should populate this volume

                csi	<CSIVolumeSource>
                  csi (Container Storage Interface) represents ephemeral storage that is
                  handled by certain external CSI drivers (Beta feature).

                downwardAPI	<DownwardAPIVolumeSource>
                  downwardAPI represents downward API about the pod that should populate this
                  volume

                emptyDir	<EmptyDirVolumeSource>
                  emptyDir represents a temporary directory that shares a pod's lifetime. More
                  info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir

                ephemeral	<EphemeralVolumeSource>
                  ephemeral represents a volume that is handled by a cluster storage driver.
                  The volume's lifecycle is tied to the pod that defines it - it will be
                  created before the pod starts, and deleted when the pod is removed.

                  Use this if: a) the volume is only needed while the pod runs, b) features of
                  normal volumes like restoring from snapshot or capacity
                     tracking are needed,
                  c) the storage driver is specified through a storage class, and d) the
                  storage driver supports dynamic volume provisioning through
                     a PersistentVolumeClaim (see EphemeralVolumeSource for more
                     information on the connection between this volume type
                     and PersistentVolumeClaim).

                  Use PersistentVolumeClaim or one of the vendor-specific APIs for volumes
                  that persist for longer than the lifecycle of an individual pod.

                  Use CSI for light-weight local ephemeral volumes if the CSI driver is meant
                  to be used that way - see the documentation of the driver for more
                  information.

                  A pod can use both types of ephemeral volumes and persistent volumes at the
                  same time.

                fc	<FCVolumeSource>
                  fc represents a Fibre Channel resource that is attached to a kubelet's host
                  machine and then exposed to the pod.

                flexVolume	<FlexVolumeSource>
                  flexVolume represents a generic volume resource that is provisioned/attached
                  using an exec based plugin.

                flocker	<FlockerVolumeSource>
                  flocker represents a Flocker volume attached to a kubelet's host machine.
                  This depends on the Flocker control service being running

                gcePersistentDisk	<GCEPersistentDiskVolumeSource>
                  gcePersistentDisk represents a GCE Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk

                gitRepo	<GitRepoVolumeSource>
                  gitRepo represents a git repository at a particular revision. DEPRECATED:
                  GitRepo is deprecated. To provision a container with a git repo, mount an
                  EmptyDir into an InitContainer that clones the repo using git, then mount
                  the EmptyDir into the Pod's container.

                glusterfs	<GlusterfsVolumeSource>
                  glusterfs represents a Glusterfs mount on the host that shares a pod's
                  lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md

                hostPath	<HostPathVolumeSource>
                  hostPath represents a pre-existing file or directory on the host machine
                  that is directly exposed to the container. This is generally used for system
                  agents or other privileged things that are allowed to see the host machine.
                  Most containers will NOT need this. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#hostpath

                iscsi	<ISCSIVolumeSource>
                  iscsi represents an ISCSI Disk resource that is attached to a kubelet's host
                  machine and then exposed to the pod. More info:
                  https://examples.k8s.io/volumes/iscsi/README.md

                name	<string> -required-
                  name of the volume. Must be a DNS_LABEL and unique within the pod. More
                  info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                nfs	<NFSVolumeSource>
                  nfs represents an NFS mount on the host that shares a pod's lifetime More
                  info: https://kubernetes.io/docs/concepts/storage/volumes#nfs

                persistentVolumeClaim	<PersistentVolumeClaimVolumeSource>
                  persistentVolumeClaimVolumeSource represents a reference to a
                  PersistentVolumeClaim in the same namespace. More info:
                  https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

                photonPersistentDisk	<PhotonPersistentDiskVolumeSource>
                  photonPersistentDisk represents a PhotonController persistent disk attached
                  and mounted on kubelets host machine

                portworxVolume	<PortworxVolumeSource>
                  portworxVolume represents a portworx volume attached and mounted on kubelets
                  host machine

                projected	<ProjectedVolumeSource>
                  projected items for all in one resources secrets, configmaps, and downward
                  API

                quobyte	<QuobyteVolumeSource>
                  quobyte represents a Quobyte mount on the host that shares a pod's lifetime

                rbd	<RBDVolumeSource>
                  rbd represents a Rados Block Device mount on the host that shares a pod's
                  lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md

                scaleIO	<ScaleIOVolumeSource>
                  scaleIO represents a ScaleIO persistent volume attached and mounted on
                  Kubernetes nodes.

                secret	<SecretVolumeSource>
                  secret represents a secret that should populate this volume. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#secret

                storageos	<StorageOSVolumeSource>
                  storageOS represents a StorageOS volume attached and mounted on Kubernetes
                  nodes.

                vsphereVolume	<VsphereVirtualDiskVolumeSource>
                  vsphereVolume represents a vSphere volume attached and mounted on kubelets
                  host machine

        """
        super().__init__(**kwargs)

        self.active_deadline_seconds = active_deadline_seconds
        self.affinity = affinity
        self.automount_service_account_token = automount_service_account_token
        self.containers = containers
        self.dns_config = dns_config
        self.dns_policy = dns_policy
        self.enable_service_links = enable_service_links
        self.ephemeral_containers = ephemeral_containers
        self.host_aliases = host_aliases
        self.host_ipc = host_ipc
        self.host_network = host_network
        self.host_pid = host_pid
        self.host_users = host_users
        self.hostname = hostname
        self.image_pull_secrets = image_pull_secrets
        self.init_containers = init_containers
        self.node_name = node_name
        self.node_selector = node_selector
        self.os = os
        self.overhead = overhead
        self.preemption_policy = preemption_policy
        self.priority = priority
        self.priority_class_name = priority_class_name
        self.readiness_gates = readiness_gates
        self.resource_claims = resource_claims
        self.restart_policy = restart_policy
        self.runtime_class_name = runtime_class_name
        self.scheduler_name = scheduler_name
        self.scheduling_gates = scheduling_gates
        self.security_context = security_context
        self.service_account = service_account
        self.service_account_name = service_account_name
        self.set_hostname_as_fqdn = set_hostname_as_fqdn
        self.share_process_namespace = share_process_namespace
        self.subdomain = subdomain
        self.termination_grace_period_seconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            if not all([
                self.containers,
            ]):
                raise MissingRequiredArgumentError(argument="containers")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["containers"] = self.containers

            if self.active_deadline_seconds:
                _spec["activeDeadlineSeconds"] = self.active_deadline_seconds

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.automount_service_account_token is not None:
                _spec["automountServiceAccountToken"] = self.automount_service_account_token

            if self.dns_config:
                _spec["dnsConfig"] = self.dns_config

            if self.dns_policy:
                _spec["dnsPolicy"] = self.dns_policy

            if self.enable_service_links is not None:
                _spec["enableServiceLinks"] = self.enable_service_links

            if self.ephemeral_containers:
                _spec["ephemeralContainers"] = self.ephemeral_containers

            if self.host_aliases:
                _spec["hostAliases"] = self.host_aliases

            if self.host_ipc is not None:
                _spec["hostIPC"] = self.host_ipc

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.host_pid is not None:
                _spec["hostPID"] = self.host_pid

            if self.host_users is not None:
                _spec["hostUsers"] = self.host_users

            if self.hostname:
                _spec["hostname"] = self.hostname

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.init_containers:
                _spec["initContainers"] = self.init_containers

            if self.node_name:
                _spec["nodeName"] = self.node_name

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.os:
                _spec["os"] = self.os

            if self.overhead:
                _spec["overhead"] = self.overhead

            if self.preemption_policy:
                _spec["preemptionPolicy"] = self.preemption_policy

            if self.priority:
                _spec["priority"] = self.priority

            if self.priority_class_name:
                _spec["priorityClassName"] = self.priority_class_name

            if self.readiness_gates:
                _spec["readinessGates"] = self.readiness_gates

            if self.resource_claims:
                _spec["resourceClaims"] = self.resource_claims

            if self.restart_policy:
                _spec["restartPolicy"] = self.restart_policy

            if self.runtime_class_name:
                _spec["runtimeClassName"] = self.runtime_class_name

            if self.scheduler_name:
                _spec["schedulerName"] = self.scheduler_name

            if self.scheduling_gates:
                _spec["schedulingGates"] = self.scheduling_gates

            if self.security_context:
                _spec["securityContext"] = self.security_context

            if self.service_account:
                _spec["serviceAccount"] = self.service_account

            if self.service_account_name:
                _spec["serviceAccountName"] = self.service_account_name

            if self.set_hostname_as_fqdn is not None:
                _spec["setHostnameAsFQDN"] = self.set_hostname_as_fqdn

            if self.share_process_namespace is not None:
                _spec["shareProcessNamespace"] = self.share_process_namespace

            if self.subdomain:
                _spec["subdomain"] = self.subdomain

            if self.termination_grace_period_seconds:
                _spec["terminationGracePeriodSeconds"] = self.termination_grace_period_seconds

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.volumes:
                _spec["volumes"] = self.volumes
