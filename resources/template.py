import json

from .resource import NamespacedResource


class Template(NamespacedResource):
    api_group = "template.openshift.io"
    singular_name = "template"

    class Labels:
        FLAVOR = "flavor.template.kubevirt.io"
        OS = "os.template.kubevirt.io"
        WORKLOAD = "workload.template.kubevirt.io"

    class Workload:
        DESKTOP = "desktop"
        HIGH_PERFORMANCE = "highperformance"
        SERVER = "server"

    class Flavor:
        LARGE = "large"
        MEDIUM = "medium"
        SMALL = "small"
        TINY = "tiny"

    def process(self, **kwargs):
        instance_dict = self.instance.to_dict()
        params = instance_dict["parameters"]
        # filling the template parameters with given kwargs
        for param in params:
            try:
                param["value"] = kwargs[param["name"]]
            except KeyError:
                continue
        instance_dict["parameters"] = params
        # TODO: remove after fix - https://issues.redhat.com/browse/KNIP-1055 (bug 1753554)
        # For template validator to be used - template namespace needs to be updated
        instance_dict["objects"][0]["metadata"]["labels"][
            "vm.kubevirt.io/template.namespace"
        ] = instance_dict["metadata"]["namespace"]
        # TODO: remove after fix - https://bugzilla.redhat.com/show_bug.cgi?id=1816518 - template
        # name needs to be updated
        instance_dict["objects"][0]["metadata"]["labels"][
            "vm.kubevirt.io/template"
        ] = instance_dict["metadata"]["name"]
        r = json.dumps(instance_dict)
        body = json.loads(r)
        response = self.client.request(
            method="Post",
            path="/apis/template.openshift.io/v1/namespaces/openshift/processedtemplates",
            body=body,
        )
        return response.to_dict()["objects"]

    @staticmethod
    def generate_template_labels(os, workload, flavor):
        return [
            f"{Template.Labels.OS}/{os}",
            f"{Template.Labels.WORKLOAD}/{getattr(Template.Workload, workload.upper())}",
            f"{Template.Labels.FLAVOR}/{getattr(Template.Flavor, flavor.upper())}",
        ]
