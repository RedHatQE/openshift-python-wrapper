# -*- coding: utf-8 -*-

import logging

from urllib3.exceptions import ProtocolError

from ocp_resources.resource import TIMEOUT, Resource
from ocp_resources.utils import TimeoutSampler


LOGGER = logging.getLogger(__name__)


class CDIConfig(Resource):
    """
    CDIConfig object.
    """

    api_group = Resource.ApiGroup.CDI_KUBEVIRT_IO

    @property
    def scratch_space_storage_class_from_spec(self):
        return self.instance.spec.scratchSpaceStorageClass

    @property
    def scratch_space_storage_class_from_status(self):
        return self.instance.status.scratchSpaceStorageClass

    @property
    def upload_proxy_url(self):
        return self.instance.status.uploadProxyURL

    def wait_until_upload_url_changed(self, uploadproxy_url, timeout=TIMEOUT):
        """
        Wait until upload proxy url is changed

        Args:
            timeout (int): Time to wait for CDI Config.

        Returns:
            bool: True if url is equal to uploadProxyURL.
        """
        LOGGER.info(
            f"Wait for {self.kind} {self.name} to ensure current URL == uploadProxyURL"
        )
        samples = TimeoutSampler(
            wait_timeout=timeout,
            sleep=1,
            exceptions=ProtocolError,
            func=self.api().get,
            field_selector=f"metadata.name=={self.name}",
        )
        for sample in samples:
            if sample.items:
                status = sample.items[0].status
                current_url = status.uploadProxyURL
                if current_url == uploadproxy_url:
                    return
