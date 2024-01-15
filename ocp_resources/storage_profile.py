# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class StorageProfile(Resource):
    """
    StorageProfile Object
    """

    api_group = Resource.ApiGroup.CDI_KUBEVIRT_IO

    def first_claim_property_set_access_modes(self):
        return self.claim_property_sets[0]['accessModes']

    def first_claim_property_set_volume_mode(self):
        return self.claim_property_sets[0]['volumeMode']

    @property
    def claim_property_sets(self):
        return self.instance.status.claimPropertySets

    @property
    def clone_strategy(self):
        return self.instance.status.get("cloneStrategy")

    @property
    def data_import_cron_source_format(self):
        return self.instance.status.get("dataImportCronSourceFormat")

    @property
    def snapshotclass(self):
        return self.instance.status.get("snapshotClass")
