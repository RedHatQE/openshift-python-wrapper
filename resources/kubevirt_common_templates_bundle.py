from .resource import NamespacedResource


class KubevirtCommonTemplatesBundle(NamespacedResource):

    api_group = NamespacedResource.ApiGroup.SSP_KUBEVIRT_IO
