# Copyright © LFV

import logging
import os

import pytest

from .reqstool.models.test_implementations import git_impl_data, implementations_data, local_impl_data, maven_impl_data
from .reqstool.models.test_imports import git_import_data, local_import_data, maven_import_data
from .reqstool.models.test_mvrs import mvr_data_1
from .reqstool.models.test_svcs import svc_data_1

# for info on # ignores for pyright and flake8 with fixtures see
# https://github.com/microsoft/pylance-release/discussions/4083

disable_loggers = ["charset_normalizer"]


def pytest_configure():
    for logger_name in disable_loggers:
        logger = logging.getLogger(logger_name)
        logger.disabled = True


def __do_not_remove_unused_imports():
    git_impl_data
    implementations_data
    local_impl_data
    maven_impl_data
    mvr_data_1
    svc_data_1
    git_import_data
    local_import_data
    maven_import_data


def __get_tests_rootdir() -> str:
    return os.path.dirname(__file__).removesuffix("/unit")


@pytest.fixture(scope="function")
def local_testdata_resources_rootdir_w_path(request) -> str:
    def closure(path):
        return os.path.join(__get_tests_rootdir(), "resources", "test_data", "data", "local", path)

    return closure


@pytest.fixture(scope="function")
def remote_testdata_resources_rootdir_w_path(request) -> str:
    def closure(path):
        return os.path.join(__get_tests_rootdir(), "resources", "test_data", "data", "remote", path)

    return closure


@pytest.fixture(scope="function")
def resource_funcname_rootdir(request) -> str:
    relative_test_file_location = (
        str(request.fspath).removeprefix(__get_tests_rootdir()).removesuffix(".py").removeprefix("/")
    )
    r_resource_funcname_rootdir = os.path.join(
        __get_tests_rootdir(), "resources", relative_test_file_location, request.function.__name__
    )

    return r_resource_funcname_rootdir


@pytest.fixture(scope="function")
def resource_funcname_rootdir_w_path(request, resource_funcname_rootdir) -> str:
    # https://www.inspiredpython.com/article/five-advanced-pytest-fixture-patterns
    def closure(path):
        return os.path.join(resource_funcname_rootdir, path)

    return closure
