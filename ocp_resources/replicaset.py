# -*- coding: utf-8 -*-
from warnings import warn
from ocp_resources.replica_set import ReplicaSet  # noqa: F401

warn(
    f"The module {__name__} is deprecated and will be removed in version 4.17, `ReplicaSet` should be imported from `ocp_resources.replica_set`",
    DeprecationWarning,
    stacklevel=2,
)
