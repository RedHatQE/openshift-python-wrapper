# -*- coding: utf-8 -*-

from typing import Any, Dict, List
from ocp_resources.resource import NamespacedResource


class ChaosEngine(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.LITMUS_IO

    class EngineStatus:
        INITIALIZED: str = "initialized"
        COMPLETED: str = "completed"
        STOPPED: str = "stopped"

    @property
    def engine_status(self) -> str:
        return self.instance.status["engineStatus"]

    @property
    def experiments_status(self) -> Dict[str, Dict[str, Any]]:
        experiments: List[Dict[Any, Any]] = self.instance.status["experiments"]
        ret_value = {}
        for experiment in experiments:
            exp = {"verdict": experiment["verdict"], "status": experiment["status"]}
            ret_value[experiment["name"]] = exp
        return ret_value

    @property
    def success(self) -> bool:
        exps = self.experiments_status
        return all(exp["verdict"] == "Pass" for exp in exps.values())
