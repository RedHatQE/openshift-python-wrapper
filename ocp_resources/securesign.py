# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class Securesign(NamespacedResource):
    """
    Securesign is the Schema for the securesigns API
    """

    api_group: str = NamespacedResource.ApiGroup.RHTAS_REDHAT_COM

    def __init__(
        self,
        ctlog: dict[str, Any] | None = None,
        fulcio: dict[str, Any] | None = None,
        rekor: dict[str, Any] | None = None,
        trillian: dict[str, Any] | None = None,
        tsa: dict[str, Any] | None = None,
        tuf: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            ctlog (dict[str, Any]): CTlogSpec defines the desired state of CTlog component

            fulcio (dict[str, Any]): FulcioSpec defines the desired state of Fulcio

            rekor (dict[str, Any]): RekorSpec defines the desired state of Rekor

            trillian (dict[str, Any]): TrillianSpec defines the desired state of Trillian

            tsa (dict[str, Any]): TimestampAuthoritySpec defines the desired state of TimestampAuthority

            tuf (dict[str, Any]): TufSpec defines the desired state of Tuf

        """
        super().__init__(**kwargs)

        self.ctlog = ctlog
        self.fulcio = fulcio
        self.rekor = rekor
        self.trillian = trillian
        self.tsa = tsa
        self.tuf = tuf

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.ctlog is not None:
                _spec["ctlog"] = self.ctlog

            if self.fulcio is not None:
                _spec["fulcio"] = self.fulcio

            if self.rekor is not None:
                _spec["rekor"] = self.rekor

            if self.trillian is not None:
                _spec["trillian"] = self.trillian

            if self.tsa is not None:
                _spec["tsa"] = self.tsa

            if self.tuf is not None:
                _spec["tuf"] = self.tuf

    # End of generated code
