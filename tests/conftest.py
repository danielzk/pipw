import os

import pkg_resources
from pkg_resources import DistributionNotFound
import pytest
import yaml

from tests.factories.packages import PkgDistributionFactory


def raise_distribution_not_found(*args, **kwargs):
    raise DistributionNotFound()


@pytest.fixture(scope='function')
def mock_pip(monkeypatch):
    monkeypatch.setattr('pip.main', lambda args: 0)
    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        lambda package: PkgDistributionFactory())


@pytest.fixture(scope='function')
def mock_pkg_dist_not_found(monkeypatch):
    monkeypatch.setattr(
        'pkg_resources.get_distribution',
        raise_distribution_not_found)


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
