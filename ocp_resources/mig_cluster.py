# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class MigCluster(NamespacedResource):
    """
    MigCluster is the Schema for the migclusters API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATION_OPENSHIFT_IO

    def __init__(
        self,
        azure_resource_group: str | None = None,
        ca_bundle: str | None = None,
        exposed_registry_path: str | None = None,
        insecure: bool | None = None,
        is_host_cluster: bool | None = None,
        refresh: bool | None = None,
        restart_restic: bool | None = None,
        service_account_secret_ref: dict[str, Any] | None = None,
        url: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            azure_resource_group (str): For azure clusters -- it's the resource group that in-cluster volumes
              use.

            ca_bundle (str): If the migcluster needs SSL verification for connections a user can
              supply a custom CA bundle. This field is required only when
              spec.Insecure is set false

            exposed_registry_path (str): Stores the path of registry route when using direct migration.

            insecure (bool): If set false, user will need to provide CA bundle for TLS connection
              to the remote cluster.

            is_host_cluster (bool): Specifies if the cluster is host (where the controller is installed)
              or not. This is a required field.

            refresh (bool): If set True, forces the controller to run a full suite of validations
              on migcluster.

            restart_restic (bool): An override setting to tell the controller that the source cluster
              restic needs to be restarted after stage pod creation.

            service_account_secret_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
              modify the referred object. --- New uses of this type are
              discouraged because of difficulty describing its usage when
              embedded in APIs.  1. Ignored fields.  It includes many fields
              which are not generally honored.  For instance, ResourceVersion
              and FieldPath are both very rarely valid in actual usage.  2.
              Invalid usage help.  It is impossible to add specific help for
              individual usage.  In most embedded usages, there are particular
              restrictions like, "must refer only to types A and B" or "UID not
              honored" or "name must be restricted".     Those cannot be well
              described when embedded.  3. Inconsistent validation.  Because the
              usages are different, the validation rules are different by usage,
              which makes it hard for users to predict what will happen.  4. The
              fields are both imprecise and overly precise.  Kind is not a
              precise mapping to a URL. This can produce ambiguity     during
              interpretation and require a REST mapping.  In most cases, the
              dependency is on the group,resource tuple     and the version of
              the actual struct is irrelevant.  5. We cannot easily change it.
              Because this type is embedded in many locations, updates to this
              type     will affect numerous schemas.  Don't make new APIs embed
              an underspecified API type they do not control.   Instead of using
              this type, create a locally provided and used type that is well-
              focused on your reference. For example, ServiceReferences for
              admission registration: https://github.com/kubernetes/api/blob/rel
              ease-1.17/admissionregistration/v1/types.go#L533 .

            url (str): Stores the url of the remote cluster. The field is only required for
              the source cluster object.

        """
        super().__init__(**kwargs)

        self.azure_resource_group = azure_resource_group
        self.ca_bundle = ca_bundle
        self.exposed_registry_path = exposed_registry_path
        self.insecure = insecure
        self.is_host_cluster = is_host_cluster
        self.refresh = refresh
        self.restart_restic = restart_restic
        self.service_account_secret_ref = service_account_secret_ref
        self.url = url

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.is_host_cluster is None:
                raise MissingRequiredArgumentError(argument="self.is_host_cluster")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["isHostCluster"] = self.is_host_cluster

            if self.azure_resource_group is not None:
                _spec["azureResourceGroup"] = self.azure_resource_group

            if self.ca_bundle is not None:
                _spec["caBundle"] = self.ca_bundle

            if self.exposed_registry_path is not None:
                _spec["exposedRegistryPath"] = self.exposed_registry_path

            if self.insecure is not None:
                _spec["insecure"] = self.insecure

            if self.refresh is not None:
                _spec["refresh"] = self.refresh

            if self.restart_restic is not None:
                _spec["restartRestic"] = self.restart_restic

            if self.service_account_secret_ref is not None:
                _spec["serviceAccountSecretRef"] = self.service_account_secret_ref

            if self.url is not None:
                _spec["url"] = self.url

    # End of generated code
