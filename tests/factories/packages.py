from collections import namedtuple

from factory import Factory

PkgDistribution = namedtuple('PkgDistribution', ['version'])


class PkgDistributionFactory(Factory):
    version = '1.0.0'

    class Meta:
        model = PkgDistribution
