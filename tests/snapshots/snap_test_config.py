# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_config_requirements 1'] = '''mylib~=1.0.0
'''

snapshots['test_config_specifier 1'] = '''mylib==1.0.0
'''

snapshots['test_config_invalid_format 1'] = '''Invalid .pipwrc
'''

snapshots['test_config_not_found 1'] = '''Config file "REMOVED_FILEPATH" not found
'''
