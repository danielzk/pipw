import pytest

from tests.conftest import config_file
from tests.utils import invoke_cli, check_requirements_snapshot


def test_no_detect_version(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a b==3.2.0 --no-detect-version', config_file)
    check_requirements_snapshot(tmpdir, snapshot)
