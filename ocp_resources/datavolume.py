"""
CDI Import
"""

import logging

import pytest
from ocp_resources.datavolume import DataVolume

from utilities.constants import TIMEOUT_1MIN, Images
from utilities.storage import (
    check_upload_virtctl_result,
    get_downloaded_artifact,
    virtctl_upload_dv,
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def upload_file_path(request, tmpdir):
    params = request.param if hasattr(request, "param") else {}
    remote_image_dir = params.get("remote_image_dir", Images.Cirros.DIR)
    remote_image_name = params.get("remote_image_name", Images.Cirros.QCOW2_IMG)
    local_name = f"{tmpdir}/{remote_image_name}"
    get_downloaded_artifact(
        remote_name=f"{remote_image_dir}/{remote_image_name}",
        local_name=local_name,
    )
    yield local_name


@pytest.fixture()
def download_specified_image(request, tmpdir_factory):
    local_path = tmpdir_factory.mktemp("cdi_upload").join(request.param.get("image_file"))
    get_downloaded_artifact(remote_name=request.param.get("image_path"), local_name=local_path)
    return local_path


@pytest.fixture()
def uploaded_dv(
    request,
    namespace,
    storage_class_name_scope_module,
    tmpdir,
):
    image_file = request.param.get("image_file")
    dv_name = image_file.split(".")[0].replace("_", "-").lower()
    local_path = f"{tmpdir}/{image_file}"
    get_downloaded_artifact(remote_name=request.param.get("remote_name"), local_name=local_path)
    with virtctl_upload_dv(
        namespace=namespace.name,
        name=dv_name,
        size=request.param.get("dv_size"),
        storage_class=storage_class_name_scope_module,
        image_path=local_path,
        insecure=True,
    ) as res:
        check_upload_virtctl_result(result=res)
        dv = DataVolume(namespace=namespace.name, name=dv_name)
        dv.wait_for_dv_success(timeout=TIMEOUT_1MIN)
        assert dv.pvc.bound(), f"PVC status is {dv.pvc.status}"
        yield dv
        dv.delete(wait=True)
