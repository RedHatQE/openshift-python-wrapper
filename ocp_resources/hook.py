import warnings
from typing import Any

from ocp_resources._hook_generated import Hook as _GeneratedHook

_UNSET = object()
_DEFAULT_IMAGE = "quay.io/konveyor/hook-runner:latest"


class Hook(_GeneratedHook):
    """
    Deprecated shim for backward compatibility.

    Preserves the legacy default-image behavior. New code should use
    ``from ocp_resources._hook_generated import Hook`` directly.
    """

    def __init__(
        self,
        aap: dict[str, Any] | None = None,
        deadline: int | None = None,
        image: Any = _UNSET,
        playbook: str | None = None,
        service_account: str | None = None,
        **kwargs: Any,
    ) -> None:
        warnings.warn(
            "Hook legacy defaults are deprecated and will be removed. "
            "Pass image= explicitly for local hooks; use aap={...} for AAP hooks.",
            DeprecationWarning,
            stacklevel=2,
        )
        if image is _UNSET:
            image = None if aap is not None else _DEFAULT_IMAGE
        super().__init__(
            aap=aap,
            deadline=deadline,
            image=image,
            playbook=playbook,
            service_account=service_account,
            **kwargs,
        )
