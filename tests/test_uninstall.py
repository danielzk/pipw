import pytest

from tests.conftest import config_file
from tests.utils import invoke_cli, check_requirements_snapshot


def test_uninstall(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-e editable1\nold1\na~=1.0.0\nold2~=1.0.0 --hash=anc\\\n--hash=abc\nb')

    invoke_cli('uninstall old1 old2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_uninstall_remove_from_all_envs(tmpdir, mock_pip, snapshot):
    paths = {
        'requirements': tmpdir.join('dev.txt'),
        'dev': tmpdir.join('dev.txt'),
        'test': tmpdir.join('test.txt'),
    }
    config = config_file(tmpdir, {
        'requirements': paths['requirements'].strpath,
        'envs': {k: v.strpath for k, v in paths.items() if k != 'requirements'},
    })

    for path in paths.values():
        path.write('old==1.0.0\na==1.0.0')

    invoke_cli('uninstall old', config)

    for path in paths.values():
        check_requirements_snapshot(tmpdir, snapshot, path)


def test_uninstall_remove_only_from_env_if_passed(tmpdir, mock_pip, snapshot):
    paths = {
        'requirements': tmpdir.join('dev.txt'),
        'dev': tmpdir.join('dev.txt'),
        'test': tmpdir.join('test.txt'),
    }
    config = config_file(tmpdir, {
        'requirements': paths['requirements'].strpath,
        'envs': {k: v.strpath for k, v in paths.items() if k != 'requirements'},
    })

    for path in paths.values():
        path.write('old==1.0.0\na==1.0.0')

    invoke_cli('uninstall old --env test', config)

    check_requirements_snapshot(tmpdir, snapshot, paths['requirements'])
    check_requirements_snapshot(tmpdir, snapshot, paths['dev'])
    check_requirements_snapshot(tmpdir, snapshot, paths['test'])


def test_uninstall_not_remove_if_no_save(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a==1.0.0\nb==1.0.0')

    invoke_cli('uninstall a b --no-save', config_file)
    check_requirements_snapshot(tmpdir, snapshot)
