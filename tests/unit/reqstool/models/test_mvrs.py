# Copyright © LFV

import pytest

from reqstool.models import mvrs


@pytest.fixture
def mvr_data_1() -> mvrs.MVRData:
    return mvrs.MVRData(
        id="MVR_001",
        svc_ids=["SVC_001", "SVC_002"],
        comment=None,
        passed=True,
    )


@pytest.fixture
def mvr_data_2() -> mvrs.MVRData:
    return mvrs.MVRData(
        id="MVR_002",
        svc_ids=["SVC_201", "SVC_202"],
        comment="Some MVR comment",
        passed=False,
    )


@pytest.fixture
def mvrs_data(mvr_data_1: mvrs.MVRData, mvr_data_2: mvrs.MVRData) -> mvrs.MVRsData:
    return mvrs.MVRsData(results={"MVR_001": mvr_data_1, "MVR_002": mvr_data_2})


def test_mvr_data(mvr_data_2: mvrs.MVRData):
    assert mvr_data_2.id == "MVR_002"
    assert mvr_data_2.svc_ids == ["SVC_201", "SVC_202"]
    assert mvr_data_2.comment == "Some MVR comment"
    assert mvr_data_2.passed is False


def test_mvrs_data(mvrs_data: mvrs.MVRsData):
    assert len(mvrs_data.results) == 2
    assert "MVR_001" in mvrs_data.results
    assert "MVR_002" in mvrs_data.results
