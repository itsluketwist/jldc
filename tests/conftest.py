import os
import shutil

import pytest


JLDC_TEST_DIRECTORY_NAME = "JLDC_TEST_DIRECTORY_NAME"


TEST_DIRECTORY = os.environ.get(JLDC_TEST_DIRECTORY_NAME, "__jldc_test_temp")


@pytest.fixture(scope="session", autouse=True)
def create_directory():
    # remove any leftover directory
    if os.path.isdir(TEST_DIRECTORY):
        shutil.rmtree(TEST_DIRECTORY)

    # create a temporary directory for testing
    os.mkdir(TEST_DIRECTORY)

    # allow testing to happen
    yield

    # clean up the directory
    if os.path.isdir(TEST_DIRECTORY):
        shutil.rmtree(TEST_DIRECTORY)
