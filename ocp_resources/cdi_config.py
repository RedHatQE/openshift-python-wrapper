# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.constants import PROTOCOL_ERROR_EXCEPTION_DICT, TIMEOUT_4MINUTES
from ocp_resources.resource import Resource
from timeout_sampler import TimeoutSampler


class CDIConfig(Resource):
    """
    CDIConfig provides a user configuration for CDI
    """

    api_group: str = Resource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        data_volume_ttl_seconds: Optional[int] = None,
        feature_gates: Optional[List[Any]] = None,
        filesystem_overhead: Optional[Dict[str, Any]] = None,
        image_pull_secrets: Optional[List[Any]] = None,
        import_proxy: Optional[Dict[str, Any]] = None,
        insecure_registries: Optional[List[Any]] = None,
        log_verbosity: Optional[int] = None,
        pod_resource_requirements: Optional[Dict[str, Any]] = None,
        preallocation: Optional[bool] = None,
        scratch_space_storage_class: Optional[str] = "",
        tls_security_profile: Optional[Dict[str, Any]] = None,
        upload_proxy_url_override: Optional[str] = "",
        **kwargs: Any,
    ) -> None:
        """
        Args:
            data_volume_ttl_seconds (int): DataVolumeTTLSeconds is the time in seconds after DataVolume
              completion it can be garbage collected. Disabled by default.

            feature_gates (List[Any]): FeatureGates are a list of specific enabled feature gates

            filesystem_overhead (Dict[str, Any]): FilesystemOverhead describes the space reserved for overhead when
              using Filesystem volumes. A value is between 0 and 1, if not
              defined it is 0.055 (5.5% overhead)

            image_pull_secrets (List[Any]): The imagePullSecrets used to pull the container images

            import_proxy (Dict[str, Any]): ImportProxy contains importer pod proxy configuration.

            insecure_registries (List[Any]): InsecureRegistries is a list of TLS disabled registries

            log_verbosity (int): LogVerbosity overrides the default verbosity level used to initialize
              loggers

            pod_resource_requirements (Dict[str, Any]): ResourceRequirements describes the compute resource requirements.

            preallocation (bool): Preallocation controls whether storage for DataVolumes should be
              allocated in advance.

            scratch_space_storage_class (str): Override the storage class to used for scratch space during transfer
              operations. The scratch space storage class is determined in the
              following order: 1. value of scratchSpaceStorageClass, if that
              doesn't exist, use the default storage class, if there is no
              default storage class, use the storage class of the DataVolume, if
              no storage class specified, use no storage class for scratch space

            tls_security_profile (Dict[str, Any]): TLSSecurityProfile is used by operators to apply cluster-wide TLS
              security settings to operands.

            upload_proxy_url_override (str): Override the URL used when uploading to a DataVolume

        """
        super().__init__(**kwargs)

        self.data_volume_ttl_seconds = data_volume_ttl_seconds
        self.feature_gates = feature_gates
        self.filesystem_overhead = filesystem_overhead
        self.image_pull_secrets = image_pull_secrets
        self.import_proxy = import_proxy
        self.insecure_registries = insecure_registries
        self.log_verbosity = log_verbosity
        self.pod_resource_requirements = pod_resource_requirements
        self.preallocation = preallocation
        self.scratch_space_storage_class = scratch_space_storage_class
        self.tls_security_profile = tls_security_profile
        self.upload_proxy_url_override = upload_proxy_url_override

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.data_volume_ttl_seconds:
                _spec["dataVolumeTTLSeconds"] = self.data_volume_ttl_seconds

            if self.feature_gates:
                _spec["featureGates"] = self.feature_gates

            if self.filesystem_overhead:
                _spec["filesystemOverhead"] = self.filesystem_overhead

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.import_proxy:
                _spec["importProxy"] = self.import_proxy

            if self.insecure_registries:
                _spec["insecureRegistries"] = self.insecure_registries

            if self.log_verbosity:
                _spec["logVerbosity"] = self.log_verbosity

            if self.pod_resource_requirements:
                _spec["podResourceRequirements"] = self.pod_resource_requirements

            if self.preallocation is not None:
                _spec["preallocation"] = self.preallocation

            if self.scratch_space_storage_class:
                _spec["scratchSpaceStorageClass"] = self.scratch_space_storage_class

            if self.tls_security_profile:
                _spec["tlsSecurityProfile"] = self.tls_security_profile

            if self.upload_proxy_url_override:
                _spec["uploadProxyURLOverride"] = self.upload_proxy_url_override

    # End of generated code

    @property
    def scratch_space_storage_class_from_spec(self) -> str:
        return self.instance.spec.scratchSpaceStorageClass

    @property
    def scratch_space_storage_class_from_status(self) -> str:
        return self.instance.status.scratchSpaceStorageClass

    @property
    def upload_proxy_url(self) -> str:
        return self.instance.status.uploadProxyURL

    def wait_until_upload_url_changed(self, uploadproxy_url: str, timeout: int = TIMEOUT_4MINUTES) -> bool:
        """
        Wait until upload proxy url is changed

        Args:
            uploadproxy_url (str): upload proxy URL
            timeout (int): Time to wait for CDI Config.

        Returns:
            bool: True if url is equal to uploadProxyURL.
        """
        self.logger.info(f"Wait for {self.kind} {self.name} to ensure current URL == uploadProxyURL")
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions_dict=PROTOCOL_ERROR_EXCEPTION_DICT,
            func=self.api.get,
            field_selector=f"metadata.name=={self.name}",
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                current_url: str = status.uploadProxyURL
                if current_url == uploadproxy_url:
                    return True

        return False
