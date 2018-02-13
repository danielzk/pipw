from tests.factories.packages import PkgDistributionFactory
from tests.utils import invoke_cli, check_requirements_snapshot


def test_install_add_requirements(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install mylib mylib2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirements(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('mylib')

    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory(version='2.0.0'))
    invoke_cli('install mylib mylib2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirements_alphabetically(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install c a b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_editables_at_start_or_after_first_hyphen_group(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a', config_file)
    invoke_cli('install -e editable1', config_file)
    invoke_cli('install b', config_file)
    invoke_cli('install --editable editable2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_after_multiline(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a==1.0 --hash=abc\\\n--hash=abc')

    invoke_cli('install b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_keep_comments(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a # Comment\n# Comment\nc=1.0')

    invoke_cli('install a b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_keep_etc(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a ; --hash=abc')

    invoke_cli('install a', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_with_specified_version(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install mylib==3.0.5', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_no_save(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a b --no-save', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists


def test_install_no_save_on_pip_error(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    monkeypatch.setattr('subprocess.call', lambda args: 1)
    invoke_cli('install a b', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists


def test_install_no_save_if_no_packages(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install -r test', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists
