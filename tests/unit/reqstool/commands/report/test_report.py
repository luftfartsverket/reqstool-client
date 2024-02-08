# Copyright © LFV


from reqstool.commands.report import report
from reqstool.locations.local_location import LocalLocation


def test_get_template_medium_ms001(local_testdata_resources_rootdir_w_path):
    rc = report.ReportCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001"))
    )
    assert rc.result


def test_get_template_standard_sys001(local_testdata_resources_rootdir_w_path):
    rc = report.ReportCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/sys-001"))
    )
    assert rc.result
