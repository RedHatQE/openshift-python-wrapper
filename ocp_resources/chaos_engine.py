# -*- coding: utf-8 -*-

from ocp_resources.resource import NamespacedResource


class ChaosEngine(NamespacedResource):

    api_group = NamespacedResource.ApiGroup.LITMUS_IO
    api_version = NamespacedResource.ApiVersion.V1ALPHA1

    class EngineStatus:
        # TODO: Rename to Uppercase
        Initialized = "initialized"
        Completed = "completed"
        Stopped = "stopped"

    @property
    def engine_status(self):
        return self.instance.status["engineStatus"]

    @property
    def experiments_status(self):
        experiments = self.instance.status["experiments"]
        ret_value = {}
        for experiment in experiments:
            exp = {"verdict": experiment["verdict"], "status": experiment["status"]}
            ret_value[experiment["name"]] = exp
        return ret_value

    @property
    def success(self):
        exps = self.experiments_status
        for exp in exps.values():
            if exp["verdict"] != "Pass":
                return False
        return True
