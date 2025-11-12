# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, NamespacedResource


class LMEvalJob(NamespacedResource):
    """
    LMEvalJob is the Schema for the lmevaljobs API
    """

    api_group: str = NamespacedResource.ApiGroup.TRUSTYAI_OPENDATAHUB_IO

    def __init__(
        self,
        allow_code_execution: bool | None = None,
        allow_online: bool | None = None,
        batch_size: str | None = None,
        chat_template: dict[str, Any] | None = None,
        gen_args: list[Any] | None = None,
        limit: str | None = None,
        log_samples: bool | None = None,
        model: str | None = None,
        model_args: list[Any] | None = None,
        num_few_shot: int | None = None,
        offline: dict[str, Any] | None = None,
        outputs: dict[str, Any] | None = None,
        pod: dict[str, Any] | None = None,
        suspend: bool | None = None,
        system_instruction: str | None = None,
        task_list: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            allow_code_execution (bool): AllowCodeExecution specifies whether the LMEvalJob can execute remote
              code. Default is false.

            allow_online (bool): AllowOnly specifies whether the LMEvalJob can directly download remote
              code, datasets and metrics. Default is false.

            batch_size (str): Batch size for the evaluation. This is used by the models that run and
              are loaded locally and not apply for the commercial APIs.

            chat_template (dict[str, Any]): ChatTemplate defines whether to apply the default or specified chat
              template to prompts. This is required for chat-completions models.

            gen_args (list[Any]): Map to `--gen_kwargs` parameter for the underlying library.

            limit (str): Accepts an integer, or a float between 0.0 and 1.0 . If passed, will
              limit the number of documents to evaluate to the first X documents
              (if an integer) per task or first X% of documents per task

            log_samples (bool): If this flag is passed, then the model's outputs, and the text fed
              into the model, will be saved at per-document granularity

            model (str): Model name

            model_args (list[Any]): Args for the model

            num_few_shot (int): Sets the number of few-shot examples to place in context

            offline (dict[str, Any]): Offline specifies settings for running LMEvalJobs in an offline mode

            outputs (dict[str, Any]): Outputs specifies storage for evaluation results

            pod (dict[str, Any]): Specify extra information for the lm-eval job's pod

            suspend (bool): Suspend keeps the job but without pods. This is intended to be used by
              the Kueue integration

            system_instruction (str): SystemInstruction will set the system instruction for all prompts
              passed to the evaluated model

            task_list (dict[str, Any]): Evaluation task list

        """
        super().__init__(**kwargs)

        self.allow_code_execution = allow_code_execution
        self.allow_online = allow_online
        self.batch_size = batch_size
        self.chat_template = chat_template
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
        self.system_instruction = system_instruction
        self.task_list = task_list

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.model is None:
                raise MissingRequiredArgumentError(argument="self.model")

            if self.task_list is None:
                raise MissingRequiredArgumentError(argument="self.task_list")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["model"] = self.model
            _spec["taskList"] = self.task_list

            if self.allow_code_execution is not None:
                _spec["allowCodeExecution"] = self.allow_code_execution

            if self.allow_online is not None:
                _spec["allowOnline"] = self.allow_online

            if self.batch_size is not None:
                _spec["batchSize"] = self.batch_size

            if self.chat_template is not None:
                _spec["chatTemplate"] = self.chat_template

            if self.gen_args is not None:
                _spec["genArgs"] = self.gen_args

            if self.limit is not None:
                _spec["limit"] = self.limit

            if self.log_samples is not None:
                _spec["logSamples"] = self.log_samples

            if self.model_args is not None:
                _spec["modelArgs"] = self.model_args

            if self.num_few_shot is not None:
                _spec["numFewShot"] = self.num_few_shot

            if self.offline is not None:
                _spec["offline"] = self.offline

            if self.outputs is not None:
                _spec["outputs"] = self.outputs

            if self.pod is not None:
                _spec["pod"] = self.pod

            if self.suspend is not None:
                _spec["suspend"] = self.suspend

            if self.system_instruction is not None:
                _spec["systemInstruction"] = self.system_instruction

    # End of generated code
