import pytest

from tests.factories.packages import PkgDistributionFactory
from tests.utils import invoke_cli, check_requirements_snapshot


def test_install_add_requirements(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirements(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a\nb==1.0.0')

    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory(version='2.0.0'))
    invoke_cli('install a b c', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirements_alphabetically(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install c a b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirements_after_last_hyphen_requirement(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-r common.txt\n-e editable1')
    invoke_cli('install a b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirements_after_last_hyphen_with_blank_lines(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-r common.txt\n\na\n--no-index\n')
    invoke_cli('install a b c', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_after_multiline(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a==1.0 --hash=abc\\\n--hash=abc')

    invoke_cli('install b', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_editables_at_start_if_no_hyphen_requirement(
        tmpdir, mock_pip, mock_pkg_dist_not_found, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a==1.0 --hash=abc\\\n--hash=abc')
    invoke_cli('install --editable editable1', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_editables_after_last_hyphen_requirement(
        tmpdir, mock_pip, mock_pkg_dist_not_found, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a==1.0 --hash=abc\\\n--hash=abc')
    invoke_cli('install -e editable1', config_file)
    invoke_cli('install b', config_file)
    invoke_cli('install --editable editable2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_editables_with_blank_lines(
        tmpdir, mock_pip, mock_pkg_dist_not_found, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-r common.txt\n\n--no-index\n')
    invoke_cli('install -e editable1', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_editables_after_multiline(
        tmpdir, mock_pip, mock_pkg_dist_not_found, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-e editable1\\\nmultiline\n')

    invoke_cli('install -e editable2 a', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_keep_comments(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a # Comment\n# Comment\nc==1.0.0\nd~=0.1.0 --hash=abc # Comment')

    invoke_cli('install a b d', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_keep_options(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a --hash=abc\nb==0.0.1 --hash=abc --hash=abc\nc >= 1.1, == 1.* --hash=abc')

    invoke_cli('install a b c==3.0.0', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_with_specified_version(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install mylib==3.0.5', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirement_with_specified_version(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a >= 1.1, == 1.*')
    invoke_cli('install a>=3.0.0', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_no_save(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a b --no-save', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists


def test_install_no_save_on_pip_error(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    monkeypatch.setattr('pip.main', lambda args: 1)
    invoke_cli('install a b', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists


def test_install_no_save_if_no_packages(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install -r test', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists


def test_install_save_mutually_exclusive_error(tmpdir, config_file, snapshot):
    result = invoke_cli('install a --save --no-save', config_file)
    snapshot.assert_match(result.output)


def test_install_set_index_url(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a -i https://index.url', config_file)
    check_requirements_snapshot(tmpdir, snapshot)
    invoke_cli('install a --index-url https://index.url2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_extra_index_url(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --extra-index-url https://index.url,https://index.url2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_not_repeat_extra_index_url(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --extra-index-url https://index.url', config_file)
    invoke_cli('install a --extra-index-url https://index.url', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_no_index(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --no-index', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_not_repeat_no_index(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --no-index', config_file)
    invoke_cli('install a --no-index', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_find_links(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --find-links https://find.links', config_file)
    invoke_cli('install a -f https://find.links2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_not_repeat_find_links(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install a --find-links https://find.links', config_file)
    invoke_cli('install a --find-links https://find.links', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_options_after_last_hyphen_requirement(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('--no-index\n-f https://find.links\n')

    invoke_cli('install a --extra-index-url https://new.last', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_options_after_multiline(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('--no-index\\\nmultiline\n')

    invoke_cli('install a --extra-index-url https://index.url', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_options_before_editables(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('--no-index\\\nmultiline\n-f https://find.links\n-e editable1')

    invoke_cli('install a --extra-index-url https://index.url', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_skip_requirements_argument(tmpdir, mock_pip, config_file, snapshot):
    invoke_cli('install -r test.txt', config_file)
    requirements_exists = tmpdir.join('requirements.txt').check()
    assert not requirements_exists

    invoke_cli('install a --requirements test.txt', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_multiline_requirement(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a~=1.0.0 --hash=abc\\\n--hash=abc')

    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory(version='2.0.0'))
    invoke_cli('install a', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_options_keep_comments(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('--index-url https://index.url # Comment')
    invoke_cli('install a --index-url https://index.url2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_with_install_option(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    invoke_cli('install a --install-option "--override-pip" --install-option "--another"', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirement_with_install_option(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a~=1.0.0 --install-option="--override-pip"')
    invoke_cli('install a --install-option "--another"', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_add_requirement_with_global_option(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    invoke_cli('install a --global-option "--override-pip" --global-option "--another"', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirement_with_global_option(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a~=1.0.0 --global-option="--override-pip"')
    invoke_cli('install a --global-option "--another"', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirements_with_hyphen(monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('a\nreq-hyp==1.0.0')

    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory(version='2.0.0'))
    invoke_cli('install a b c', config_file)
    check_requirements_snapshot(tmpdir, snapshot)


def test_install_update_requirements_with_different_letter_case(
        monkeypatch, tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('Django==1.0.0\nmylib')

    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory(version='2.0.0'))
    invoke_cli('install django Mylib', config_file)
    check_requirements_snapshot(tmpdir, snapshot)
