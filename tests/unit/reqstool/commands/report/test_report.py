# Copyright © LFV

from reqstool_python_decorators.decorators.decorators import SVCs
from reqstool.commands.report import report
from reqstool.commands.report.criterias.group_by import GroupbyOptions
from reqstool.commands.report.criterias.sort_by import SortByOptions
from reqstool.locations.local_location import LocalLocation


@SVCs("SVC_038", "SVC_039", "SVC_041")
def test_get_template_medium_ms001(local_testdata_resources_rootdir_w_path):
    rc = report.ReportCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        group_by=GroupbyOptions.CATEGORY,
        sort_by=[SortByOptions.ID],
    )
    assert rc.result


@SVCs("SVC_038", "SVC_040", "SVC_042")
def test_get_template_standard_sys001(local_testdata_resources_rootdir_w_path):
    rc = report.ReportCommand(
        location=LocalLocation(
            path=local_testdata_resources_rootdir_w_path("test_standard/baseline/sys-001"),
        ),
        group_by=GroupbyOptions.INITIAL_IMPORTS,
        sort_by=[SortByOptions.SIGNIFICANCE],
    )
    assert rc.result
