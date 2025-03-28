# API reference: https://tekton.dev/docs/pipelines/pipelineruns/

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class PipelineRun(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.TEKTON_DEV

    def __init__(
        self,
        pipelineref=None,
        params=None,
        service_account_name=None,
        **kwargs,
    ):
        """
        Args:
            pipelineref (str): Mandatory: Base pipeline to run pipelineruns
            params (dict): Optional params to add during triggering a run.
            params can be set/changed based on pipelineref.
            example : params={"param_name1":"param_value1", "param_name2":"param_value2"}
            service_account_name (str): Optional to provide service account
        """
        super().__init__(**kwargs)
        self.pipelineref = pipelineref
        self.params = params
        self.service_account_name = service_account_name

    def to_dict(self) -> None:
        super().to_dict()
        if not self.kind_dict and not self.yaml_file:
            if not self.pipelineref:
                raise MissingRequiredArgumentError(argument="pipelineref")
            self.res["spec"] = {}
            self.res["spec"]["pipelineref"] = {"name": self.pipelineref}

            if self.params:
                self.res["spec"]["params"] = [
                    {"name": params_name, "value": params_value} for params_name, params_value in self.params.items()
                ]

            if self.service_account_name:
                self.res["spec"]["serviceAccountName"] = self.service_account_name
