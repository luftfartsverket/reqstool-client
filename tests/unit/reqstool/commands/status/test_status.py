# Copyright © LFV
from reqstool_python_decorators.decorators.decorators import SVCs

from reqstool.commands.status.status import StatusCommand
from reqstool.locations.local_location import LocalLocation


@SVCs("SVC_021")
def test_status_incomplete_implementation(local_testdata_resources_rootdir_w_path):
    result = StatusCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001"))
    )

    status, nr_of_incomplete_requirements = result.result

    assert nr_of_incomplete_requirements == 5


@SVCs("SVC_021")
def test_status_report_generation_sys_ms(local_testdata_resources_rootdir_w_path):
    result = StatusCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/empty_ms/ms-001"))
    )

    status, nr_of_incomplete_requirements = result.result

    assert nr_of_incomplete_requirements == 5
