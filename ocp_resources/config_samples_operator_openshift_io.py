# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import Resource


class Config(Resource):
    """
       Config contains the configuration and detailed condition status for the Samples Operator.
    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.SAMPLES_OPERATOR_OPENSHIFT_IO

    def __init__(
        self,
        architectures: list[Any] | None = None,
        management_state: str | None = None,
        samples_registry: str | None = None,
        skipped_imagestreams: list[Any] | None = None,
        skipped_templates: list[Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            architectures (list[Any]): architectures determine which hardware architecture(s) to install,
              where x86_64, ppc64le, and s390x are the only supported choices
              currently.

            management_state (str): managementState is top level on/off type of switch for all operators.
              When "Managed", this operator processes config and manipulates the
              samples accordingly. When "Unmanaged", this operator ignores any
              updates to the resources it watches. When "Removed", it reacts
              that same wasy as it does if the Config object is deleted, meaning
              any ImageStreams or Templates it manages (i.e. it honors the
              skipped lists) and the registry secret are deleted, along with the
              ConfigMap in the operator's namespace that represents the last
              config used to manipulate the samples,

            samples_registry (str): samplesRegistry allows for the specification of which registry is
              accessed by the ImageStreams for their image content.  Defaults on
              the content in https://github.com/openshift/library that are
              pulled into this github repository, but based on our pulling only
              ocp content it typically defaults to registry.redhat.io.

            skipped_imagestreams (list[Any]): skippedImagestreams specifies names of image streams that should NOT
              be created/updated.  Admins can use this to allow them to delete
              content they don’t want.  They will still have to manually delete
              the content but the operator will not recreate(or update) anything
              listed here.

            skipped_templates (list[Any]): skippedTemplates specifies names of templates that should NOT be
              created/updated.  Admins can use this to allow them to delete
              content they don’t want.  They will still have to manually delete
              the content but the operator will not recreate(or update) anything
              listed here.

        """
        super().__init__(**kwargs)

        self.architectures = architectures
        self.management_state = management_state
        self.samples_registry = samples_registry
        self.skipped_imagestreams = skipped_imagestreams
        self.skipped_templates = skipped_templates

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.architectures is not None:
                _spec["architectures"] = self.architectures

            if self.management_state is not None:
                _spec["managementState"] = self.management_state

            if self.samples_registry is not None:
                _spec["samplesRegistry"] = self.samples_registry

            if self.skipped_imagestreams is not None:
                _spec["skippedImagestreams"] = self.skipped_imagestreams

            if self.skipped_templates is not None:
                _spec["skippedTemplates"] = self.skipped_templates

    # End of generated code
