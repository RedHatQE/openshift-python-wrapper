# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class MigAnalytic(NamespacedResource):
    """
    MigAnalytic is the Schema for the miganalytics API
    """

    api_group: str = NamespacedResource.ApiGroup.MIGRATION_OPENSHIFT_IO

    def __init__(
        self,
        analyze_extended_pv_capacity: bool | None = None,
        analyze_image_count: bool | None = None,
        analyze_k8s_resources: bool | None = None,
        analyze_pv_capacity: bool | None = None,
        list_images: bool | None = None,
        list_images_limit: int | None = None,
        mig_plan_ref: dict[str, Any] | None = None,
        refresh: bool | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            analyze_extended_pv_capacity (bool): Enables advanced analysis of volumes required for PV resizing

            analyze_image_count (bool): Enables analysis of image count, if set true. This is a required
              field.

            analyze_k8s_resources (bool): Enables analysis of k8s resources, if set true. This is a required
              field.

            analyze_pv_capacity (bool): Enables analysis of persistent volume capacity, if set true. This is a
              required field.

            list_images (bool): Enable used in analysis of image count, if set true.

            list_images_limit (int): Represents limit on image counts

            mig_plan_ref (dict[str, Any]): ObjectReference contains enough information to let you inspect or
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

            refresh (bool): Enables refreshing existing MigAnalytic

        """
        super().__init__(**kwargs)

        self.analyze_extended_pv_capacity = analyze_extended_pv_capacity
        self.analyze_image_count = analyze_image_count
        self.analyze_k8s_resources = analyze_k8s_resources
        self.analyze_pv_capacity = analyze_pv_capacity
        self.list_images = list_images
        self.list_images_limit = list_images_limit
        self.mig_plan_ref = mig_plan_ref
        self.refresh = refresh

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.analyze_image_count is None:
                raise MissingRequiredArgumentError(argument="self.analyze_image_count")

            if self.analyze_k8s_resources is None:
                raise MissingRequiredArgumentError(argument="self.analyze_k8s_resources")

            if self.analyze_pv_capacity is None:
                raise MissingRequiredArgumentError(argument="self.analyze_pv_capacity")

            if self.mig_plan_ref is None:
                raise MissingRequiredArgumentError(argument="self.mig_plan_ref")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["analyzeImageCount"] = self.analyze_image_count
            _spec["analyzeK8SResources"] = self.analyze_k8s_resources
            _spec["analyzePVCapacity"] = self.analyze_pv_capacity
            _spec["migPlanRef"] = self.mig_plan_ref

            if self.analyze_extended_pv_capacity is not None:
                _spec["analyzeExtendedPVCapacity"] = self.analyze_extended_pv_capacity

            if self.list_images is not None:
                _spec["listImages"] = self.list_images

            if self.list_images_limit is not None:
                _spec["listImagesLimit"] = self.list_images_limit

            if self.refresh is not None:
                _spec["refresh"] = self.refresh

    # End of generated code
