import os
import pkg_resources
import subprocess

import pytest

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

    file_ = tmpdir.join('.pipwrc')

    requirements = config.get('requirements', None)
    specifier = config.get('specifier', None)

    if not requirements:
        requirements = tmpdir.join('requirements.txt').strpath
    file_.write('requirements: {}'.format(requirements))

    if specifier:
        file_.write('specifier: {}'.format(specifier))

    return file_
