# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_uninstall 1'] = '''-e editable1
a~=1.0.0
b'''

snapshots['test_uninstall_remove_from_all_envs 1'] = 'a==1.0.0'

snapshots['test_uninstall_remove_from_all_envs 2'] = 'a==1.0.0'

snapshots['test_uninstall_remove_from_all_envs 3'] = 'a==1.0.0'

snapshots['test_uninstall_not_remove_if_no_save 1'] = '''a==1.0.0
b==1.0.0'''

snapshots['test_uninstall_remove_only_from_env_if_passed 1'] = '''old==1.0.0
a==1.0.0'''

snapshots['test_uninstall_remove_only_from_env_if_passed 2'] = '''old==1.0.0
a==1.0.0'''

snapshots['test_uninstall_remove_only_from_env_if_passed 3'] = '''a==1.0.0'''
