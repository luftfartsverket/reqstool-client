# Copyright © LFV

from reqstool.commands.status.statistics_container import (
    CombinedRequirementTestItem,
    StatisticsContainer,
    TestStatisticsItem,
    TotalStatisticsItem,
)
from reqstool.commands.status.statistics_generator import StatisticsGenerator
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.local_location import LocalLocation


def test_calculate_test_basic(local_testdata_resources_rootdir_w_path):
    result: StatisticsContainer = StatisticsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_basic/baseline/ms-101")),
        semantic_validator=SemanticValidator(validation_error_holder=ValidationErrorHolder()),
    ).result

    expected = StatisticsContainer(
        _requirement_statistics={
            UrnId(urn="ms-101", id="REQ_101"): CombinedRequirementTestItem(
                completed=True,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ms-101", id="REQ_102"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ms-101", id="REQ_201"): CombinedRequirementTestItem(
                completed=True,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
            ),
            UrnId(urn="ms-101", id="REQ_202"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
            ),
        },
        _total_statistics=TotalStatisticsItem(
            nr_of_failed_tests=2,
            nr_of_missing_tests=0,
            nr_of_skipped_tests=0,
            nr_of_passed_tests=2,
            nr_of_total_tests=4,
            nr_of_completed_requirements=2,
            nr_of_total_requirements=4,
            nr_of_reqs_with_implementation=2,
        ),
    )
    assert result == expected


# @pytest.mark.skip(reason="Might be testdata error. Need to investigate")
def test_calculate_test_standard_ms001(local_testdata_resources_rootdir_w_path):
    result: StatisticsContainer = StatisticsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/baseline/ms-001")),
        semantic_validator=SemanticValidator(validation_error_holder=ValidationErrorHolder()),
    ).result

    expected = StatisticsContainer(
        _requirement_statistics={
            UrnId(urn="ms-001", id="REQ_ms001_101"): CombinedRequirementTestItem(
                completed=True,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=2,
                    nr_of_total_tests=2,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ms-001", id="REQ_ms001_102"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
            ),
            UrnId(urn="sys-001", id="REQ_sys001_103"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=2,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-001", id="REQ_ext001_101"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=1,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=2,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_101"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_102"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_103"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
        },
        _total_statistics=TotalStatisticsItem(
            nr_of_failed_tests=2,
            nr_of_missing_tests=2,
            nr_of_skipped_tests=0,
            nr_of_passed_tests=4,
            nr_of_total_tests=8,
            nr_of_completed_requirements=1,
            nr_of_total_requirements=7,
            nr_of_reqs_with_implementation=4,
        ),
    )
    assert result == expected


def test_calculate_empty_standard_ms001(local_testdata_resources_rootdir_w_path):
    result: StatisticsContainer = StatisticsGenerator(
        initial_location=LocalLocation(path=local_testdata_resources_rootdir_w_path("test_standard/empty_ms/ms-001")),
        semantic_validator=SemanticValidator(validation_error_holder=ValidationErrorHolder()),
    ).result

    expected = StatisticsContainer(
        _requirement_statistics={
            UrnId(urn="sys-001", id="REQ_sys001_101"): CombinedRequirementTestItem(
                completed=True,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=2,
                    nr_of_total_tests=2,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="sys-001", id="REQ_sys001_102"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=1,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=3,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=2,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=3,
                    not_applicable=False,
                ),
            ),
            UrnId(urn="sys-001", id="REQ_sys001_103"): CombinedRequirementTestItem(
                completed=True,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=1,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
            ),
            UrnId(urn="ext-001", id="REQ_ext001_101"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=1,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=2,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=2,
                    nr_of_total_tests=5,
                    not_applicable=False,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=1,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=1,
                    not_applicable=False,
                ),
            ),
            UrnId(urn="ext-001", id="REQ_ext001_103"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_101"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_102"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
            UrnId(urn="ext-002", id="REQ_ext002_103"): CombinedRequirementTestItem(
                completed=False,
                nr_of_implementations=0,
                automated_tests_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
                mvrs_stats=TestStatisticsItem(
                    nr_of_failed_tests=0,
                    nr_of_missing_tests=0,
                    nr_of_skipped_tests=0,
                    nr_of_passed_tests=0,
                    nr_of_total_tests=0,
                    not_applicable=True,
                ),
            ),
        },
        _total_statistics=TotalStatisticsItem(
            nr_of_failed_tests=3,
            nr_of_missing_tests=2,
            nr_of_skipped_tests=0,
            nr_of_passed_tests=6,
            nr_of_total_tests=11,
            nr_of_completed_requirements=2,
            nr_of_total_requirements=8,
            nr_of_reqs_with_implementation=4,
        ),
    )
    assert result == expected