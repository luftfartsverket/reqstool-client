# Copyright © LFV

import logging
from enum import Enum
from typing import Dict, List
from pathlib import Path

from jinja2 import (
    BaseLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    TemplateNotFound,
    select_autoescape,
)

from reqstool.commands.status.statistics_container import StatisticsContainer
from reqstool.commands.status.statistics_generator import StatisticsGenerator
from reqstool.common.dataclasses.urn_id import UrnId
from reqstool.common.validator_error_holder import ValidationErrorHolder
from reqstool.common.validators.semantic_validator import SemanticValidator
from reqstool.locations.location import LocationInterface
from reqstool.model_generators.combined_indexed_dataset_generator import CombinedIndexedDatasetGenerator
from reqstool.model_generators.combined_raw_datasets_generator import CombinedRawDatasetsGenerator
from reqstool.models.annotations import AnnotationData
from reqstool.models.combined_indexed_dataset import CombinedIndexedDataset
from reqstool.models.mvrs import MVRData
from reqstool.models.svcs import SVCData
from reqstool.models.test_data import TestRunStatus


class TemplateNames(Enum):
    REQUIREMENTS = "requirements"
    SVCS = "svcs"
    ANNOTATION_IMPLS = "annotation_impls"
    ANNOTATION_TESTS = "annotation_tests"
    MVRS = "mvrs"
    REQ_REFERENCES = "req_references"
    TOTAL_STATISTICS = "total_statistics"


class ReportCommand:
    def __init__(self, location: LocationInterface):
        self.__initial_location: LocationInterface = location
        self.templates = {}
        self.result = self.__run()

    # call on Jinja2 template with reportmodel
    def __create_template(self, template_name: str) -> Template:
        """Returns a Template based on the template name

        Args:
            template_name (str): The name of the template to retrieve

        Returns:
            Template: Jinja2 template used for rendering of the AsciiDoc document
        """

        def load_template(loader: BaseLoader) -> Template:
            template_env = Environment(
                loader=loader, autoescape=select_autoescape(), trim_blocks=True, lstrip_blocks=True
            )
            return template_env.get_template(template_name)

        try:
            p = Path(__file__).parent / "templates"
            fs_loader = FileSystemLoader(searchpath=p)
            return load_template(fs_loader)
        except TemplateNotFound:
            logging.info("Can't find local files. Uses package loader instead.")

            package_loader = PackageLoader("reqstool")
            return load_template(package_loader)

    def __render(self, imported_models, template: Template) -> str:
        """Returns a string with rendered template as an AsciiDoc Document

        Args:
            imported_models: Model(s) to render
            template (Template): Template to base the rendering upon

        Returns:
            str: The rendered template
        """

        return template.render(report=imported_models)

    def __run(self) -> str:
        semantic_validator = SemanticValidator(validation_error_holder=ValidationErrorHolder())
        # generate datasets
        crd = CombinedRawDatasetsGenerator(
            initial_location=self.__initial_location, semantic_validator=semantic_validator
        ).combined_raw_datasets
        cid: CombinedIndexedDataset = CombinedIndexedDatasetGenerator(_crd=crd).combined_indexed_dataset
        # generate all reqs templates
        all_reqs = {"initial_model": crd.initial_model_urn, "templates": self.__create_requirements_container(cid=cid)}

        # build statistics
        statistics: StatisticsContainer = StatisticsGenerator(
            initial_location=self.__initial_location, semantic_validator=semantic_validator
        ).result
        # build templates
        self.templates[TemplateNames.REQUIREMENTS] = self.__create_template("requirements.j2")
        self.templates[TemplateNames.SVCS] = self.__create_template("svcs.j2")
        self.templates[TemplateNames.ANNOTATION_TESTS] = self.__create_template("annotation_tests.j2")
        self.templates[TemplateNames.ANNOTATION_IMPLS] = self.__create_template("annotation_impls.j2")
        self.templates[TemplateNames.MVRS] = self.__create_template("mvrs.j2")
        self.templates[TemplateNames.REQ_REFERENCES] = self.__create_template("req_references.j2")
        self.templates[TemplateNames.TOTAL_STATISTICS] = self.__create_template("total_statistics.j2")

        report = self.__generate_asciidoc_information(all_reqs, statistics)

        return report

    def __generate_asciidoc_information(self, reqs, statistics: StatisticsContainer):
        """Parses the read data from the imported models and creates a AsciiDoc string

        Args:
            imported_models: All models that should be converted to AsciiDoc

        Returns:
            str : All data rendered as AsciiDoc
        """
        statistics_table = self.__render(statistics._total_statistics, self.templates[TemplateNames.TOTAL_STATISTICS])

        result = "== REQUIREMENT DOCUMENTATION\n"
        initial = "=== INITIAL REQUIREMENTS\n"
        imported = "=== IMPORTED REQUIREMENTS\n"
        # we should start to generate requirements defined in inital source
        for req_template in reqs["templates"]:
            if reqs["initial_model"] == req_template["urn"]:
                initial += self.__extract_template_data(req_template=req_template)
            else:
                imported += self.__extract_template_data(req_template=req_template)
        return result + statistics_table + initial + imported

    def __extract_template_data(self, req_template) -> str:
        requirement_as_asciidoc = ""
        req_as_ascii = self.__render(req_template["requirement"], self.templates[TemplateNames.REQUIREMENTS])
        annot_impls_as_ascii = self.__render(req_template["impls"], self.templates[TemplateNames.ANNOTATION_IMPLS])
        annot_tests_as_ascii = self.__render(req_template["tests"], self.templates[TemplateNames.ANNOTATION_TESTS])
        svcs_as_ascii = self.__render(req_template["svcs"], self.templates[TemplateNames.SVCS])
        mvrs_to_ascii = self.__render(req_template["mvrs"], self.templates[TemplateNames.MVRS])
        requirement_as_asciidoc += (
            req_as_ascii
            + (annot_impls_as_ascii if annot_impls_as_ascii else "")
            + (svcs_as_ascii if svcs_as_ascii else "")
            + (annot_tests_as_ascii if annot_tests_as_ascii else "")
            + (mvrs_to_ascii if mvrs_to_ascii else "")
            + "\n"
        )
        return requirement_as_asciidoc

    def __create_requirements_container(self, cid: CombinedIndexedDataset) -> List:
        requirement_data = []
        for urn_id, req_data in cid.requirements.items():
            # Get all svc UrnIds related to current requirement
            svcs_urn_ids: List[UrnId] = self._get_urn_ids_for_svcs(
                urn_id=urn_id, svcs_from_req=cid.svcs_from_req.items()
            )

            # Get svcs for current requirement
            svcs: List[SVCData] = [cid.svcs[urn_id] for urn_id in svcs_urn_ids]

            # Get all verification types for current req
            verifications_as_string = ", ".join(str(svc.verification.value) for svc in svcs)

            # get all implementations for current requirement
            impls: List = self._get_annotation_impls(cid=cid, urn_id=urn_id)

            mvr_ids: List[UrnId] = self._get_mvr_ids_for_req(cid=cid, svcs_urn_ids=svcs_urn_ids)

            # Get mvrs for current requirement if there are any (else [])
            mvrs: List[MVRData] = self._get_mvrs_for_req(mvrs=cid.mvrs, mvr_ids=mvr_ids)

            # generate templates for tests related to current requirement
            automated_test_results: List = self._get_annotated_automated_test_results_for_req(
                cid=cid, svcs_urn_ids=svcs_urn_ids
            )

            req_temp_data = {
                "id": urn_id.id,
                "title": req_data.title,
                "description": req_data.description,
                "rationale": req_data.rationale,
                "verification": verifications_as_string,
                "req_refs": req_data.references,
            }

            data_container = {
                "urn": urn_id.urn,
                "requirement": req_temp_data,
                "impls": impls,
                "svcs": svcs,
                "tests": automated_test_results,
                "mvrs": mvrs,
            }

            requirement_data.append(data_container)

        return requirement_data

    def _get_urn_ids_for_svcs(self, urn_id: UrnId, svcs_from_req: Dict[UrnId, List[UrnId]]) -> List[UrnId]:
        svcs_urn_ids: List[UrnId] = []
        for req_urn_id, svc_list in svcs_from_req:
            if urn_id == req_urn_id:
                for svc in svc_list:
                    svcs_urn_ids.append(svc)
        return svcs_urn_ids

    def _get_mvr_ids_for_req(self, cid: CombinedIndexedDataset, svcs_urn_ids: List[UrnId]) -> List[UrnId]:
        mvr_ids: List[UrnId] = []
        for svc_urn_id in svcs_urn_ids:
            for id, value in cid.mvrs_from_svc.items():
                if id == svc_urn_id:
                    for urn in value:
                        mvr_ids.append(urn)
        return mvr_ids

    def _get_mvrs_for_req(self, mvrs: Dict[UrnId, MVRData], mvr_ids: List[UrnId]) -> List[MVRData]:
        return [mvrs[mvr_id] for mvr_id in mvr_ids] if mvr_ids else []

    def _get_annotated_automated_test_results_for_req(
        self,
        cid: CombinedIndexedDataset,
        svcs_urn_ids: List[UrnId],
    ) -> List:
        automated_test_results = []
        for urn_id in svcs_urn_ids:
            if urn_id in cid.annotations_tests:
                annotations = cid.annotations_tests[urn_id]
                for tests in annotations:
                    for test in tests:
                        test_urn_id = UrnId(urn=urn_id.urn, id=test.fully_qualified_name)
                        results = self.__get_annotated_test_results(cid=cid, urn_id=test_urn_id)
                        results_as_string = ", ".join(str(result.status.value) for result in results)
                        annot_test = {
                            "svc_id": urn_id.id,
                            "element_kind": test.element_kind,
                            "fqn": test.fully_qualified_name,
                            "test_result": results_as_string,
                        }
                        automated_test_results.append(annot_test)

        return automated_test_results

    def __get_annotated_test_results(self, cid: CombinedIndexedDataset, urn_id: UrnId) -> List[TestRunStatus]:
        test_results: List[TestRunStatus] = []
        # do lookup for each test from previous method, and if result is missing, add a Missing status
        if urn_id in cid.automated_test_result:
            tests = cid.automated_test_result[urn_id]
            for test in tests:
                test_results.append(test)
        else:
            test_results.append(TestRunStatus.MISSING)

        return test_results

    def _get_annotation_impls(self, cid: CombinedIndexedDataset, urn_id: UrnId):
        impls_list = []
        impls_for_urn: List[AnnotationData] = cid.annotations_impls[urn_id] if urn_id in cid.annotations_impls else []
        if impls_for_urn:
            for impls in impls_for_urn:
                for impl in impls:
                    impl_template = {"element_kind": impl.element_kind, "fqn": impl.fully_qualified_name}
                    impls_list.append(impl_template)

        return impls_list
