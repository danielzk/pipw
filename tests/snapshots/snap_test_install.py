# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_install_add_requirements 1'] = '''mylib~=1.0.0
mylib2~=1.0.0
'''

snapshots['test_install_update_requirements 1'] = '''mylib~=2.0.0
mylib2~=2.0.0'''

snapshots['test_install_add_requirements_alphabetically 1'] = '''a~=1.0.0
b~=1.0.0
c~=1.0.0
'''

snapshots['test_install_add_editables_at_start_or_after_first_hyphen_group 1'] = '''-e editable1~=1.0.0
-e editable2~=1.0.0
a~=1.0.0
b~=1.0.0
'''

snapshots['test_install_add_requirement_after_multiline 1'] = '''a==1.0 --hash=abc\\
--hash=abc
b~=1.0.0'''

snapshots['test_install_keep_comments 1'] = '''a~=1.0.0 # Comment
b~=1.0.0
# Comment
c=1.0'''

snapshots['test_install_keep_etc 1'] = 'a~=1.0.0 ; --hash=abc'

snapshots['test_install_add_requirement_with_specified_version 1'] = '''mylib==3.0.5
'''
