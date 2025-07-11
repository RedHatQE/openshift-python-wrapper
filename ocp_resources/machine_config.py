from typing import Any

from ocp_resources.resource import Resource


class MachineConfig(Resource):
    """
    https://docs.openshift.com/container-platform/4.16/rest_api/machine_apis/machineconfig-machineconfiguration-openshift-io-v1.html
    """

    api_group = Resource.ApiGroup.MACHINECONFIGURATION_OPENSHIFT_IO

    def __init__(
        self,
        os_image_url: str | None = None,
        config: dict[str, Any] | None = None,
        kernel_arguments: list[str] | None = None,
        extensions: list[str] | None = None,
        fips: bool | None = None,
        kernel_type: str | None = None,
        base_os_extensions_container_image: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            os_image_url (str, optional): URL to the OS image.
            config (dict, optional): Ignition config file data.
                Example:
                {
                    "ignition": {
                        "version": "3.1.0",
                        "config": {
                            "merge": [
                                {
                                    "source": "http://path/to/your/config.ign"
                                }
                            ]
                        }
                    },
                    "storage": {
                        "filesystems": [
                            {
                                "name": "root",
                                "mount": {
                                    "device": "/dev/disk/by-label/root",
                                    "format": "xfs",
                                    "wipeFilesystem": False
                                }
                            }
                        ]
                    }
                }
            kernel_arguments (list, optional): list of kernel arguments.
            extensions (list, optional): list of extensions to install.
            fips (bool, optional): Enable FIPS mode. Defaults to False.
            kernel_type (str, optional): Type of kernel to use.
            base_os_extensions_container_image (str, optional): URL to the base OS extensions container image.
        """
        super().__init__(**kwargs)
        self.os_image_url = os_image_url
        self.config = config
        self.kernel_arguments = kernel_arguments
        self.extensions = extensions
        self.fips = fips
        self.kernel_type = kernel_type
        self.base_os_extensions_container_image = base_os_extensions_container_image

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.os_image_url:
                _spec["osImageURL"] = self.os_image_url

            if self.config:
                _spec["config"] = self.config

            if self.kernel_arguments:
                _spec["kernelArguments"] = self.kernel_arguments

            if self.extensions:
                _spec["extensions"] = self.extensions

            if self.fips is not None:
                _spec["fips"] = self.fips

            if self.kernel_type:
                _spec["kernelType"] = self.kernel_type

            if self.base_os_extensions_container_image:
                _spec["baseOSExtensionsContainerImage"] = self.base_os_extensions_container_image
