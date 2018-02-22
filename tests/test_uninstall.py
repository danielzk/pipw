import pytest

from tests.utils import invoke_cli, check_requirements_snapshot


def test_uninstall(tmpdir, mock_pip, config_file, snapshot):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('-e editable1\nold1\na~=1.0.0\nold2~=1.0.0 --hash=anc\\\n--hash=abc\nb')

    invoke_cli('uninstall old1 old2', config_file)
    check_requirements_snapshot(tmpdir, snapshot)
