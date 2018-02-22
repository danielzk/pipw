import pytest

from tests.conftest import config_file
from tests.utils import invoke_cli, check_requirements_snapshot


def test_save_to(tmpdir, mock_pip, config_file, snapshot):
    requirements_path = tmpdir.join('custom.txt')
    invoke_cli('install a --save-to {}'.format(requirements_path.strpath), config_file)
    check_requirements_snapshot(tmpdir, snapshot, requirements_path)


def test_save_to_and_env_mutually_exclusive_error(tmpdir, mock_pip, config_file, snapshot):
    result = invoke_cli('install a --save-to file --env abc', config_file)
    assert result.exit_code != 0
    snapshot.assert_match(result.output)
