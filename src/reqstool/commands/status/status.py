# Copyright © LFV

from typing import List, Tuple

from colorama import Fore, Style
from tabulate import tabulate

from reqstool.commands.status.statistics_container import StatisticsContainer, TestStatisticsItem
from reqstool.commands.status.statistics_generator import StatisticsGenerator
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.location import LocationInterface


class StatusCommand:
    def __init__(self, location: LocationInterface):
        self.__initial_location: LocationInterface = location
        self.result = self.__status_result()

    def __status_result(self) -> Tuple[str, int]:
        statistics: StatisticsContainer = StatisticsGenerator(
            initial_location=self.__initial_location,
            semantic_validator=SemanticValidator(validation_error_holder=ValidationErrorHolder()),
        ).result
        status = _status_table(stats_container=statistics)

        return (
            status,
            statistics._total_statistics.nr_of_total_requirements
            - statistics._total_statistics.nr_of_completed_requirements,
        )


def _build_table(req_id: str, urn: str, impls: int, tests: str, mvrs: str, completed: bool) -> List[str]:
    row = [urn]
    # add color to requirement if it's completed or not
    req_id_color = f"{Fore.GREEN}" if completed else f"{Fore.RED}"
    row.append(f"{req_id_color}{req_id}{Style.RESET_ALL}")
    # perform check for impls
    row.extend([Fore.GREEN + "Implemented" + Style.RESET_ALL if impls > 0 else Fore.RED + "Missing" + Style.RESET_ALL])
    _extend_row(tests, row)
    _extend_row(mvrs, row)
    return row


# builds the status table
def _status_table(stats_container: StatisticsContainer) -> str:
    table_data = []
    headers = ["URN", "Req Id", "Implementation", "Automated Test", "Manual Test"]
    title = "\nSTATUS"

    for req, stats in stats_container._requirement_statistics.items():
        table_data.append(
            _build_table(
                req_id=req.id,
                urn=req.urn,
                impls=stats.nr_of_implementations,
                tests=stats.automated_tests_stats,
                mvrs=stats.mvrs_stats,
                completed=stats.completed,
            )
        )

    col_align = ["center"] * len(table_data[0])
    table = tabulate(tablefmt="fancy_grid", tabular_data=table_data, headers=headers, colalign=col_align)
    table_with_title = f"{title}\n{table}\n"
    statisics = _summarize_statisics(
        nr_of_total_reqs=stats_container._total_statistics.nr_of_total_requirements,
        nr_of_completed_reqs=stats_container._total_statistics.nr_of_completed_requirements,
        implemented=stats_container._total_statistics.nr_of_reqs_with_implementation,
        left_to_implement=stats_container._total_statistics.nr_of_total_requirements
        - stats_container._total_statistics.nr_of_reqs_with_implementation,
        total_tests=stats_container._total_statistics.nr_of_total_tests,
        passed_tests=stats_container._total_statistics.nr_of_passed_tests,
        failed_tests=stats_container._total_statistics.nr_of_failed_tests,
        skipped_tests=stats_container._total_statistics.nr_of_skipped_tests,
        missing_automated_tests=stats_container._total_statistics.nr_of_missing_automated_tests,
        missing_manual_tests=stats_container._total_statistics.nr_of_missing_manual_tests,
        nr_of_total_svcs=stats_container._total_statistics.nr_of_total_svcs,
    )

    legend = [
        [
            "T = Total",
            Fore.GREEN + "P = Passed" + Style.RESET_ALL,
            Fore.RED + "F = Failed" + Style.RESET_ALL,
            Fore.YELLOW + "S = Skipped" + Style.RESET_ALL,
            Fore.RED + "M = Missing" + Style.RESET_ALL,
        ],
    ]

    legend_table_data = tabulate(tablefmt="fancy_grid", tabular_data=legend)

    status = table_with_title + legend_table_data + statisics

    return status


def _summarize_statisics(
    nr_of_total_reqs: int,
    nr_of_completed_reqs: int,
    implemented: int,
    left_to_implement: int,
    total_tests: int,
    passed_tests: int,
    failed_tests: int,
    skipped_tests: int,
    missing_automated_tests: int,
    missing_manual_tests: int,
    nr_of_total_svcs: int,
) -> str:
    header_req_data = ("\b" * len(str(nr_of_total_reqs))) + f"Total Requirements: {str(nr_of_total_reqs)}"
    header_test_data = ("\b" * len(str(total_tests))) + f"Total Tests: {str(total_tests)}"
    header_svcs_data = ("\b" * len(str(nr_of_total_svcs))) + f"Total SVCs: {str(nr_of_total_svcs)}"

    table_req_data = [
        [
            str(nr_of_completed_reqs)
            + __numbers_as_percentage(numerator=nr_of_completed_reqs, denominator=nr_of_total_reqs),
            str(implemented - nr_of_completed_reqs)
            + __numbers_as_percentage(numerator=implemented - nr_of_completed_reqs, denominator=nr_of_total_reqs),
            str(left_to_implement) + __numbers_as_percentage(numerator=left_to_implement, denominator=nr_of_total_reqs),
        ]
    ]
    table_svc_data = [
        [
            str(passed_tests) + __numbers_as_percentage(numerator=passed_tests, denominator=total_tests),
            str(failed_tests) + __numbers_as_percentage(numerator=failed_tests, denominator=total_tests),
            str(skipped_tests) + __numbers_as_percentage(numerator=skipped_tests, denominator=total_tests),
            str(missing_automated_tests)
            + __numbers_as_percentage(numerator=missing_automated_tests, denominator=nr_of_total_svcs),
            str(missing_manual_tests)
            + __numbers_as_percentage(numerator=missing_manual_tests, denominator=nr_of_total_svcs),
        ]
    ]
    req_headers = [
        "Implemented and Verified",
        "Implemented",
        "Not implemented",
    ]
    svc_headers = [
        "Passed tests",
        "Failed tests",
        "Skipped tests",
        "SVCs missing tests",
        "SVCs missing MVRs",
    ]
    col_align = ["center"] * len(table_req_data[0])
    req_table = req_table = tabulate(
        tablefmt="fancy_grid",
        tabular_data=table_req_data,
        headers=req_headers,
        colalign=col_align,
    )
    svc_table = svc_table = tabulate(
        tablefmt="fancy_grid",
        tabular_data=table_svc_data,
        headers=svc_headers,
        colalign=col_align,
    )

    total_req_header = (
        "╒════════════════════════════════════════════════════════════════╕"
        f"\n│                      {header_req_data}                      │"
        "\n╘════════════════════════════════════════════════════════════════╛"
    )

    total_tests_svcs_header = (
        "╒═══════════════════════════════════════════════════╤════════════════════════════════════════════╕"
        f"\n│                   {header_test_data}                   │"
        f"                {header_svcs_data}                │"
        "\n╘═══════════════════════════════════════════════════╧════════════════════════════════════════════╛"
    )

    table_with_title = f"\n{total_req_header}\n{req_table}\n{total_tests_svcs_header}\n{svc_table}"

    return table_with_title


def __numbers_as_percentage(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    percentage = (numerator / denominator) * 100
    percentage_as_string = " ({:.2f}%)".format(percentage)
    return percentage_as_string


def _extend_row(result: TestStatisticsItem, row: List[str]):
    colored_item = ""
    if result.not_applicable:
        colored_item = f"{'N/A'}"
    else:
        colored_item = f"{'T'}{str(result.nr_of_total_tests)}"

    if result.nr_of_passed_tests > 0:
        colored_item += f"{Fore.GREEN}{' P'}{str(result.nr_of_passed_tests)}{Style.RESET_ALL}"
    if result.nr_of_failed_tests > 0:
        colored_item += f"{Fore.RED}{' F'}{str(result.nr_of_failed_tests)}{Style.RESET_ALL}"
    if result.nr_of_skipped_tests > 0:
        colored_item += f"{Fore.YELLOW}{' S'}{str(result.nr_of_skipped_tests)}{Style.RESET_ALL}"

    if result.nr_of_missing_automated_tests > 0:
        colored_item += f"{Fore.RED}{' M'}{str(result.nr_of_missing_automated_tests)}{Style.RESET_ALL}"

    if result.nr_of_missing_manual_tests > 0:
        colored_item += f"{Fore.RED}{' M'}{str(result.nr_of_missing_manual_tests)}{Style.RESET_ALL}"

    row.append(colored_item)
