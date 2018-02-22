# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_save_to 1'] = '''a~=1.0.0
'''

snapshots['test_save_to_and_env_mutually_exclusive_error 1'] = '''--env and --save-to options are mutually exclusive
'''
