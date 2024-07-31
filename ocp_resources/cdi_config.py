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
        feature_gates: Optional[Dict[str, Any]] = None,
        filesystem_overhead: Optional[Dict[str, Any]] = None,
        image_pull_secrets: Optional[List[Any]] = None,
        import_proxy: Optional[Dict[str, Any]] = None,
        insecure_registries: Optional[Dict[str, Any]] = None,
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
            data_volume_ttl_seconds(int): DataVolumeTTLSeconds is the time in seconds after DataVolume completion it
              can be garbage collected. Disabled by default.

            feature_gates(Dict[Any, Any]): FeatureGates are a list of specific enabled feature gates

            filesystem_overhead(Dict[Any, Any]): FilesystemOverhead describes the space reserved for overhead when using
              Filesystem volumes. A value is between 0 and 1, if not defined it is 0.055
              (5.5% overhead)

              FIELDS:
                global	<string>
                  Global is how much space of a Filesystem volume should be reserved for
                  overhead. This value is used unless overridden by a more specific value (per
                  storageClass)

                storageClass	<map[string]string>
                  StorageClass specifies how much space of a Filesystem volume should be
                  reserved for safety. The keys are the storageClass and the values are the
                  overhead. This value overrides the global value

            image_pull_secrets(List[Any]): The imagePullSecrets used to pull the container images
              LocalObjectReference contains enough information to let you locate the
              referenced object inside the same namespace.

              FIELDS:
                name	<string>
                  Name of the referent.
                  This field is effectively required, but due to backwards compatibility is
                  allowed to be empty. Instances of this type with an empty value here are
                  almost certainly wrong.
                  TODO: Add other useful fields. apiVersion, kind, uid?
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Drop `kubebuilder:default` when controller-gen doesn't need it
                  https://github.com/kubernetes-sigs/kubebuilder/issues/3896.

            import_proxy(Dict[Any, Any]): ImportProxy contains importer pod proxy configuration.

              FIELDS:
                HTTPProxy	<string>
                  HTTPProxy is the URL http://<username>:<pswd>@<ip>:<port> of the import
                  proxy for HTTP requests.  Empty means unset and will not result in the
                  import pod env var.

                HTTPSProxy	<string>
                  HTTPSProxy is the URL https://<username>:<pswd>@<ip>:<port> of the import
                  proxy for HTTPS requests.  Empty means unset and will not result in the
                  import pod env var.

                noProxy	<string>
                  NoProxy is a comma-separated list of hostnames and/or CIDRs for which the
                  proxy should not be used. Empty means unset and will not result in the
                  import pod env var.

                trustedCAProxy	<string>
                  TrustedCAProxy is the name of a ConfigMap in the cdi namespace that contains
                  a user-provided trusted certificate authority (CA) bundle.
                  The TrustedCAProxy ConfigMap is consumed by the DataImportCron controller
                  for creating cronjobs, and by the import controller referring a copy of the
                  ConfigMap in the import namespace.
                  Here is an example of the ConfigMap (in yaml):


                  apiVersion: v1
                  kind: ConfigMap
                  metadata:
                    name: my-ca-proxy-cm
                    namespace: cdi
                  data:
                    ca.pem: |
                      -----BEGIN CERTIFICATE-----
                             ... <base64 encoded cert> ...
                             -----END CERTIFICATE-----

            insecure_registries(Dict[Any, Any]): InsecureRegistries is a list of TLS disabled registries

            log_verbosity(int): LogVerbosity overrides the default verbosity level used to initialize
              loggers

            pod_resource_requirements(Dict[Any, Any]): ResourceRequirements describes the compute resource requirements.

              FIELDS:
                claims	<[]Object>
                  Claims lists the names of resources, defined in spec.resourceClaims,
                  that are used by this container.


                  This is an alpha field and requires enabling the
                  DynamicResourceAllocation feature gate.


                  This field is immutable. It can only be set for containers.

                limits	<map[string]Object>
                  Limits describes the maximum amount of compute resources allowed.
                  More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                requests	<map[string]Object>
                  Requests describes the minimum amount of compute resources required.
                  If Requests is omitted for a container, it defaults to Limits if that is
                  explicitly specified,
                  otherwise to an implementation-defined value. Requests cannot exceed Limits.
                  More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

            preallocation(bool): Preallocation controls whether storage for DataVolumes should be allocated
              in advance.

            scratch_space_storage_class(str): Override the storage class to used for scratch space during transfer
              operations. The scratch space storage class is determined in the following
              order: 1. value of scratchSpaceStorageClass, if that doesn't exist, use the
              default storage class, if there is no default storage class, use the storage
              class of the DataVolume, if no storage class specified, use no storage class
              for scratch space

            tls_security_profile(Dict[Any, Any]): TLSSecurityProfile is used by operators to apply cluster-wide TLS security
              settings to operands.

              FIELDS:
                custom	<Object>
                  custom is a user-defined TLS security profile. Be extremely careful using a
                  custom
                  profile as invalid configurations can be catastrophic. An example custom
                  profile
                  looks like this:


                    ciphers:
                      - ECDHE-ECDSA-CHACHA20-POLY1305
                      - ECDHE-RSA-CHACHA20-POLY1305
                      - ECDHE-RSA-AES128-GCM-SHA256
                      - ECDHE-ECDSA-AES128-GCM-SHA256
                    minTLSVersion: VersionTLS11

                intermediate	<Object>
                  intermediate is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Intermediate_compatibility_.28recommended.29


                  and looks like this (yaml):


                    ciphers:
                      - TLS_AES_128_GCM_SHA256
                      - TLS_AES_256_GCM_SHA384
                      - TLS_CHACHA20_POLY1305_SHA256
                      - ECDHE-ECDSA-AES128-GCM-SHA256
                      - ECDHE-RSA-AES128-GCM-SHA256
                      - ECDHE-ECDSA-AES256-GCM-SHA384
                      - ECDHE-RSA-AES256-GCM-SHA384
                      - ECDHE-ECDSA-CHACHA20-POLY1305
                      - ECDHE-RSA-CHACHA20-POLY1305
                      - DHE-RSA-AES128-GCM-SHA256
                      - DHE-RSA-AES256-GCM-SHA384
                    minTLSVersion: VersionTLS12

                modern	<Object>
                  modern is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility


                  and looks like this (yaml):


                    ciphers:
                      - TLS_AES_128_GCM_SHA256
                      - TLS_AES_256_GCM_SHA384
                      - TLS_CHACHA20_POLY1305_SHA256
                    minTLSVersion: VersionTLS13


                  NOTE: Currently unsupported.

                old	<Object>
                  old is a TLS security profile based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Old_backward_compatibility


                  and looks like this (yaml):


                    ciphers:
                      - TLS_AES_128_GCM_SHA256
                      - TLS_AES_256_GCM_SHA384
                      - TLS_CHACHA20_POLY1305_SHA256
                      - ECDHE-ECDSA-AES128-GCM-SHA256
                      - ECDHE-RSA-AES128-GCM-SHA256
                      - ECDHE-ECDSA-AES256-GCM-SHA384
                      - ECDHE-RSA-AES256-GCM-SHA384
                      - ECDHE-ECDSA-CHACHA20-POLY1305
                      - ECDHE-RSA-CHACHA20-POLY1305
                      - DHE-RSA-AES128-GCM-SHA256
                      - DHE-RSA-AES256-GCM-SHA384
                      - DHE-RSA-CHACHA20-POLY1305
                      - ECDHE-ECDSA-AES128-SHA256
                      - ECDHE-RSA-AES128-SHA256
                      - ECDHE-ECDSA-AES128-SHA
                      - ECDHE-RSA-AES128-SHA
                      - ECDHE-ECDSA-AES256-SHA384
                      - ECDHE-RSA-AES256-SHA384
                      - ECDHE-ECDSA-AES256-SHA
                      - ECDHE-RSA-AES256-SHA
                      - DHE-RSA-AES128-SHA256
                      - DHE-RSA-AES256-SHA256
                      - AES128-GCM-SHA256
                      - AES256-GCM-SHA384
                      - AES128-SHA256
                      - AES256-SHA256
                      - AES128-SHA
                      - AES256-SHA
                      - DES-CBC3-SHA
                    minTLSVersion: VersionTLS10

                type	<string>
                  type is one of Old, Intermediate, Modern or Custom. Custom provides
                  the ability to specify individual TLS security profile parameters.
                  Old, Intermediate and Modern are TLS security profiles based on:


                  https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_configurations


                  The profiles are intent based, so they may change over time as new ciphers
                  are developed and existing ciphers
                  are found to be insecure.  Depending on precisely which ciphers are
                  available to a process, the list may be
                  reduced.


                  Note that the Modern profile is currently not supported because it is not
                  yet well adopted by common software libraries.

            upload_proxy_url_override(str): Override the URL used when uploading to a DataVolume

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

        if not self.yaml_file:
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
