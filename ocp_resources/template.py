import json

from ocp_resources.resource import NamespacedResource


class Template(NamespacedResource):
    api_group = NamespacedResource.ApiGroup.TEMPLATE_OPENSHIFT_IO
    singular_name = "template"

    class Labels:
        BASE = f"{NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO}/type=base"
        FLAVOR = "flavor.template.kubevirt.io"
        OS = "os.template.kubevirt.io"
        WORKLOAD = "workload.template.kubevirt.io"

    class Workload:
        DESKTOP = "desktop"
        HIGHPERFORMANCE = "highperformance"
        SERVER = "server"

    class Flavor:
        LARGE = "large"
        MEDIUM = "medium"
        SMALL = "small"
        TINY = "tiny"

    class Annotations:
        DEPRECATED = f"{NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO}/deprecated"
        PROVIDER = f"{NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO}/provider"
        PROVIDER_SUPPORT_LEVEL = (
            f"{NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO}/provider-support-level"
        )
        PROVIDER_URL = (
            f"{NamespacedResource.ApiGroup.TEMPLATE_KUBEVIRT_IO}/provider-url"
        )

    class VMAnnotations:
        OS = f"{NamespacedResource.ApiGroup.VM_KUBEVIRT_IO}/os"
        FLAVOR = f"{NamespacedResource.ApiGroup.VM_KUBEVIRT_IO}/flavor"
        WORKLOAD = f"{NamespacedResource.ApiGroup.VM_KUBEVIRT_IO}/workload"

    def process(self, client=None, **kwargs):
        client = client or self.client
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
        instance_json = json.dumps(instance_dict)
        body = json.loads(instance_json)
        response = client.request(
            method="Post",
            path=f"/apis/{self.api_version}/namespaces/openshift/processedtemplates",
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
