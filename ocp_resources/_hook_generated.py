# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Hook(NamespacedResource):
    """
    Hook is the Schema for the hooks API
    """

    api_group: str = NamespacedResource.ApiGroup.FORKLIFT_KONVEYOR_IO

    def __init__(
        self,
        aap: dict[str, Any] | None = None,
        deadline: int | None = None,
        image: str | None = None,
        playbook: str | None = None,
        service_account: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            aap (dict[str, Any]): AAP (Ansible Automation Platform) configuration for remote job
              execution. When specified, the hook will trigger an AAP job
              template instead of running a local playbook.

            deadline (int): Hook deadline in seconds.

            image (str): Image to run the hook workload (required for local hooks; omit for AAP
              hooks).

            playbook (str): A base64 encoded Ansible playbook (optional for local hooks; when set,
              ansible-runner is used).

            service_account (str): Service account.

        """
        super().__init__(**kwargs)

        self.aap = aap
        self.deadline = deadline
        self.image = image
        self.playbook = playbook
        self.service_account = service_account

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.aap is not None:
                _spec["aap"] = self.aap

            if self.deadline is not None:
                _spec["deadline"] = self.deadline

            if self.image is not None:
                _spec["image"] = self.image

            if self.playbook is not None:
                _spec["playbook"] = self.playbook

            if self.service_account is not None:
                _spec["serviceAccount"] = self.service_account

    # End of generated code
