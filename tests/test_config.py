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
