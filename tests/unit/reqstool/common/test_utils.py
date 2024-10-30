# Copyright © LFV


from reqstool.common.utils import Utils


def test_create_accessible_nodes_dict():
    parsing_graph: dict = {
        "ext-001": [],
        "ext-002": [],
        "sys-001": ["ext-001", "ext-002", "ms-001"],
        "ms-001": ["sys-001"],
    }

    accesible_nodes_dict = Utils.create_accessible_nodes_dict(parsing_graph)

    assert accesible_nodes_dict
