# Copyright © LFV

from reqstool.commands.generate_json.generate_json import GenerateJsonCommand
from reqstool.locations.local_location import LocalLocation


def test_generate_json(local_testdata_resources_rootdir_w_path):
    gjc = GenerateJsonCommand(
        location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        filter_data=True,
    )
    assert gjc.result
