# Copyright © LFV

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

from reqstool_python_decorators.decorators.decorators import Requirements

from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.models.test_data import TEST_RUN_STATUS, TestData, TestsData


class TestDataModelGenerator:
    UNIT_METHOD_IDENTIFIER_REGEX = r"^([a-zA-Z_$][a-zA-Z0-9_$]*).*$"
    KARATE_METHOD_IDENTIFIER_REGEX = r"\[\d+(?:\.\d+)?:\d+\]\s*(.+)"

    def __init__(self, path: str, urn: str):
        self.path = path
        self.urn = urn
        # key: urn+fqn
        self.model: Dict[UrnId, TestData] = self.__generate(path, urn)

    def __generate(self, path: str, urn: str) -> TestsData:
        tests = self.__parse_test_data(path, urn)

        return TestsData(tests=tests)

    @Requirements("REQ_014", "REQ_015")
    def __parse_test_data(self, path: str, urn: str) -> Dict[str, TestData]:
        r_testdata: Dict[str, TestData] = {}

        xml_files = list(Path(path).glob("**/*.xml"))

        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for testcase in root.findall(".//testcase"):
                # Check if there is a match
                match_unit = re.match(self.UNIT_METHOD_IDENTIFIER_REGEX, testcase.attrib["name"])
                match_karate = re.match(self.KARATE_METHOD_IDENTIFIER_REGEX, testcase.attrib["name"])

                if match_unit:
                    methodname = match_unit.group(1)
                elif match_karate:
                    methodname = match_karate.group(1)
                else:
                    logging.error(f"{testcase.attrib['name']} is not a valid method name\n")
                    methodname = "invalid_method_name"

                test_run_status: TEST_RUN_STATUS

                if testcase.find("./failure") is not None:
                    test_run_status = TEST_RUN_STATUS.FAILED
                elif testcase.find("./skipped") is not None:
                    test_run_status = TEST_RUN_STATUS.SKIPPED
                else:
                    test_run_status = TEST_RUN_STATUS.PASSED

                fqn = f"{testcase.attrib['classname']}.{methodname}"

                test_data = TestData(fully_qualified_name=fqn, status=test_run_status)
                urn_id = UrnId(urn=urn, id=fqn)
                r_testdata[urn_id] = test_data

        return r_testdata
