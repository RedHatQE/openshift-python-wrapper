# Reference Doc: https://github.com/metallb/metallb-operator/blob/main/api/v1beta1/metallb_types.go

from ocp_resources.resource import NamespacedResource


class MetalLB(NamespacedResource):
    """
    MetalLB object.
    """

    api_group = NamespacedResource.ApiGroup.METALLB_IO

    def __init__(
        self,
        name=None,
        namespace=None,
        client=None,
        log_level="info",
        speaker_config=None,
        speaker_tolerations=None,
        **kwargs,
    ):
        """
        Args:
            name (str): Name of the MetalLB or it's CR's.
            namespace (str): Namespace of the MetalLB
            client: (DynamicClient): DynamicClient to use.
            log_level(str): The verbosity of the controller and the speaker logging.
                            Allowed values are: all, debug, info, warn, error, none. (default: info)
            speaker_config (dict): Additional configs to be applied on MetalLB Speaker daemonset.
            speaker_tolerations (list): List of tolerations to be applied on Speaker Daemonset.
        """
        super().__init__(
            name=name,
            namespace=namespace,
            client=client,
            **kwargs,
        )
        self.log_level = log_level
        self.speaker_config = speaker_config
        self.speaker_tolerations = speaker_tolerations

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            self.res["spec"]["logLevel"] = self.log_level

            if self.speaker_config:
                self.res["spec"]["speakerConfig"] = self.speaker_config

            if self.speaker_tolerations:
                self.res["spec"]["speakerTolerations"] = self.speaker_tolerations
