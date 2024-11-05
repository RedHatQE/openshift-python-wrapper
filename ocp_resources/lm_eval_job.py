# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource, MissingRequiredArgumentError


class LMEvalJob(NamespacedResource):
    """
    LMEvalJob is the Schema for the lmevaljobs API
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        batch_size: Optional[str] = "",
        gen_args: Optional[List[Any]] = None,
        limit: Optional[str] = "",
        log_samples: Optional[bool] = None,
        model: Optional[str] = "",
        model_args: Optional[List[Any]] = None,
        num_few_shot: Optional[int] = None,
        offline: Optional[Dict[str, Any]] = None,
        outputs: Optional[Dict[str, Any]] = None,
        pod: Optional[Dict[str, Any]] = None,
        suspend: Optional[bool] = None,
        task_list: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            batch_size (str): Batch size for the evaluation. This is used by the models that run and
              are loaded locally and not apply for the commercial APIs.

            gen_args (List[Any]): Map to `--gen_kwargs` parameter for the underlying library.

            limit (str): Accepts an integer, or a float between 0.0 and 1.0 . If passed, will
              limit the number of documents to evaluate to the first X documents
              (if an integer) per task or first X% of documents per task

            log_samples (bool): If this flag is passed, then the model's outputs, and the text fed
              into the model, will be saved at per-document granularity

            model (str): Model name

            model_args (List[Any]): Args for the model

            num_few_shot (int): Sets the number of few-shot examples to place in context

            offline (Dict[str, Any]): Offline specifies settings for running LMEvalJobs in a offline mode

            outputs (Dict[str, Any]): Outputs specifies storage for evaluation results

            pod (Dict[str, Any]): Specify extra information for the lm-eval job's pod

            suspend (bool): Suspend keeps the job but without pods. This is intended to be used by
              the Kueue integration

            task_list (Dict[str, Any]): Evaluation task list

        """
        super().__init__(**kwargs)

        self.batch_size = batch_size
        self.gen_args = gen_args
        self.limit = limit
        self.log_samples = log_samples
        self.model = model
        self.model_args = model_args
        self.num_few_shot = num_few_shot
        self.offline = offline
        self.outputs = outputs
        self.pod = pod
        self.suspend = suspend
        self.task_list = task_list

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if not self.model:
                raise MissingRequiredArgumentError(argument="self.model")

            if not self.task_list:
                raise MissingRequiredArgumentError(argument="self.task_list")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["model"] = self.model
            _spec["taskList"] = self.task_list

            if self.batch_size:
                _spec["batchSize"] = self.batch_size

            if self.gen_args:
                _spec["genArgs"] = self.gen_args

            if self.limit:
                _spec["limit"] = self.limit

            if self.log_samples is not None:
                _spec["logSamples"] = self.log_samples

            if self.model_args:
                _spec["modelArgs"] = self.model_args

            if self.num_few_shot:
                _spec["numFewShot"] = self.num_few_shot

            if self.offline:
                _spec["offline"] = self.offline

            if self.outputs:
                _spec["outputs"] = self.outputs

            if self.pod:
                _spec["pod"] = self.pod

            if self.suspend is not None:
                _spec["suspend"] = self.suspend

    # End of generated code
