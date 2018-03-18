from os.path import join, dirname
from subprocess import Popen, PIPE
import sys

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup
from setuptools.command.install import install

current_dir = dirname(__file__)

reqs_file = join(current_dir, 'requirements', 'common.txt')
reqs = parse_requirements(reqs_file, session=PipSession())
install_requires = [str(req.req) for req in reqs]

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
        'verify': VerifyVersionCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
