import pytest

from tests.conftest import config_file
from tests.utils import invoke_cli, check_requirements_snapshot


def test_config_requirements(tmpdir, mock_pip, snapshot):
    requirements_path = tmpdir.join('custom', 'path.txt')
    config = config_file(tmpdir, {'requirements': requirements_path.strpath})
    invoke_cli('install mylib', config)
    check_requirements_snapshot(tmpdir, snapshot, requirements_path)


def test_config_specifier(tmpdir, mock_pip, snapshot):
    config = config_file(tmpdir, {'specifier': '=='})
    invoke_cli('install mylib', config)
    check_requirements_snapshot(tmpdir, snapshot)


def test_config_invalid_format(tmpdir, snapshot):
    file_ = tmpdir.join('.pipwrc')
    file_.write('invalid=format[asdsdasd]')
    result = invoke_cli('install mylib', file_)
    assert result.exit_code != 0
    snapshot.assert_match(result.output)


def test_config_not_found(tmpdir, snapshot):
    file_ = tmpdir.join('.pipwrc')
    result = invoke_cli('install mylib', file_)
    assert result.exit_code != 0
    snapshot.assert_match(result.output.replace(file_.strpath, 'REMOVED_FILEPATH'))


def test_config_env(tmpdir, mock_pip, snapshot):
    requirements_path = tmpdir.join('requirements.txt')
    dev_requirements_path = tmpdir.join('dev.txt')
    config = config_file(tmpdir, {
        'requirements': requirements_path.strpath,
        'envs': {
            'dev': dev_requirements_path.strpath,
        },
    })
    invoke_cli('install a --env dev', config)
    invoke_cli('install b -m dev', config)

    requirements_exists = requirements_path.check()
    assert not requirements_exists
    check_requirements_snapshot(tmpdir, snapshot, dev_requirements_path)


def test_config_should_display_error_if_invalid_env(tmpdir, mock_pip, config_file, snapshot):
    result = invoke_cli('install a --env abc', config_file)
    assert result.exit_code != 0
    snapshot.assert_match(result.output)


def test_config_detect_version(tmpdir, mock_pip, snapshot):
    config = config_file(tmpdir, {'detect_version': 'false'})
    invoke_cli('install a b==3.2.0', config)
    check_requirements_snapshot(tmpdir, snapshot)
