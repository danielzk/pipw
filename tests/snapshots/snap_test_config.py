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

snapshots['test_config_env 1'] = '''a~=1.0.0
b~=1.0.0
'''

snapshots['test_config_should_display_error_if_invalid_env 1'] = '''Environmment "abc" not found
'''
