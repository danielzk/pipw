from os.path import join, dirname
import platform
from subprocess import Popen, PIPE
import sys

import pip
from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup
from setuptools.command.install import install

current_dir = dirname(__file__)
is_windows = platform.system() == 'Windows'

reqs_file = join(current_dir, 'requirements', 'common.txt')
reqs = parse_requirements(reqs_file, session=PipSession())
reqs = [str(req.req) for req in reqs]

with open(join(current_dir, 'VERSION')) as version_file:
    version = version_file.read().strip()

with open(join(current_dir, 'README.rst')) as readme_file:
    long_description = readme_file.read()

console_scripts = ['pipw = pipw.main:cli']


class VerifyVersionCommand(install):
    description = 'Verify that the git tag matches our version'

    def run(self):
        args = 'git describe --abbrev=0 --tags'.split()
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        tag, err = p.communicate()
        if p.returncode:
            sys.exit('Git tag not found')

        tag = tag.decode('utf-8').strip()
        if tag != version:
            msg = 'Git tag "{}" does not match the current version "{}"'.format(
                tag, version)
            sys.exit(msg)


class CustomInstall(install):
    user_options = install.user_options + [
        ('override-pip', 'o', 'Override pip command'),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.override_pip = None

    def run(self):
        # Install dependencies in this way due to a bug with --install-option.
        # See <https://github.com/pypa/pip/issues/4338>.
        if not is_windows:
            pip.main(['install'] + reqs)

        if self.override_pip:
            console_scripts.append('pip = pipw.main:cli')

        install.run(self)


install_requires = []
if is_windows:
    install_requires = reqs

setup(
    name='pipw',
    version=version,
    author='Daniel Ramos',
    author_email='danielrz@protonmail.com',
    description='A wrapper for pip to save packages in requirements files.',
    license='MIT',
    keywords='pip save requirements npm',
    url='https://github.com/danielzk/pipw',
    packages=['pipw'],
    entry_points = {'console_scripts': console_scripts},
    long_description=long_description,
    install_requires=install_requires,
    cmdclass={
        'install': CustomInstall,
        'verify': VerifyVersionCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
