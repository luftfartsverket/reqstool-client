# Copyright © LFV


from reqstool.locations.local_location import LocalLocation


def test_local_location(resource_funcname_rootdir_w_path):
    PATH = "/tmp/somepath"

    local_location = LocalLocation(path=PATH)

    assert local_location.path == PATH
