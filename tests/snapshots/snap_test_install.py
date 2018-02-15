# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_install_add_requirements 1'] = '''a~=1.0.0
b~=1.0.0
'''

snapshots['test_install_update_requirements 1'] = '''a~=2.0.0
b~=2.0.0'''

snapshots['test_install_add_requirements_alphabetically 1'] = '''a~=1.0.0
b~=1.0.0
c~=1.0.0
'''

snapshots['test_install_add_requirements_after_last_hyphen_requirement 1'] = '''-r common.txt
-e editable1
a~=1.0.0
b~=1.0.0'''

snapshots['test_install_add_requirements_after_last_hyphen_with_blank_lines 1'] = '''-r common.txt

a~=1.0.0
--no-index
b~=1.0.0
c~=1.0.0
'''

snapshots['test_install_add_requirement_after_multiline 1'] = '''a==1.0 --hash=abc\\
--hash=abc
b~=1.0.0'''

snapshots['test_install_add_editables_at_start_if_no_hyphen_requirement 1'] = '''-e editable1
a==1.0 --hash=abc\\
--hash=abc'''

snapshots['test_install_add_editables_after_last_hyphen_requirement 1'] = '''-e editable1
-e editable2
a==1.0 --hash=abc\\
--hash=abc
b'''

snapshots['test_install_add_editables_with_blank_lines 1'] = '''-r common.txt

--no-index
-e editable1
'''

snapshots['test_install_add_editables_after_multiline 1'] = '''-e editable1\\
multiline
-e editable2
a
'''

snapshots['test_install_keep_comments 1'] = '''a~=1.0.0 # Comment
b~=1.0.0
# Comment
c=1.0'''

snapshots['test_install_keep_etc 1'] = '''a~=1.0.0 ; --hash=abc
b~=1.0.0 ; --hash=abc
c==3.0.0 ; --hash=abc'''

snapshots['test_install_add_requirement_with_specified_version 1'] = '''mylib==3.0.5
'''

snapshots['test_install_update_requirement_with_specified_version 1'] = 'a>=3.0.0'

snapshots['test_install_save_mutually_exclusive_error 1'] = '''--save and --no-save options are mutually exclusive
'''

snapshots['test_install_set_index_url 1'] = '''-i https://index.url
a~=1.0.0
'''

snapshots['test_install_set_index_url 2'] = '''-i https://index.url2
a~=1.0.0'''

snapshots['test_install_add_extra_index_url 1'] = '''--extra-index-url https://index.url
--extra-index-url https://index.url2
a~=1.0.0
'''

snapshots['test_install_not_repeat_extra_index_url 1'] = '''--extra-index-url https://index.url
a~=1.0.0
'''

snapshots['test_install_add_no_index 1'] = '''--no-index
a~=1.0.0
'''

snapshots['test_install_not_repeat_no_index 1'] = '''--no-index
a~=1.0.0
'''

snapshots['test_install_add_find_links 1'] = '''-f https://find.links
-f https://find.links2
a~=1.0.0
'''

snapshots['test_install_not_repeat_find_links 1'] = '''-f https://find.links
a~=1.0.0
'''

snapshots['test_install_add_options_after_last_hyphen_requirement 1'] = '''--no-index
-f https://find.links
--extra-index-url https://new.last
a~=1.0.0
'''

snapshots['test_install_add_options_after_multiline 1'] = '''--no-index\\
multiline
--extra-index-url https://index.url
a~=1.0.0
'''

snapshots['test_install_add_options_before_editables 1'] = '''--no-index\\
multiline
-f https://find.links
--extra-index-url https://index.url
-e editable1
a~=1.0.0'''
