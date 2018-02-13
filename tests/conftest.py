import os
import pkg_resources
import subprocess

import pytest
import yaml

from tests.factories.packages import PkgDistributionFactory


@pytest.fixture(scope='function')
def mock_pip(monkeypatch):
    monkeypatch.setattr('subprocess.call', lambda args: 0)
    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory())


@pytest.fixture(scope='function')
def config_file(tmpdir, config=None):
    if config is None:
        config = {}

    if not config.get('requirements', None):
        config['requirements'] = tmpdir.join('requirements.txt').strpath

    output = yaml.dump(config)
    file_ = tmpdir.join('.pipwrc')
    file_.write(output)

    return file_
