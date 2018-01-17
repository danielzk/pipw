from collections import namedtuple, OrderedDict
import os
from os.path import join
import pkg_resources
from pkg_resources import RequirementParseError, DistributionNotFound
import re
import sys
import subprocess

import click

default_config = {
    'default_file': join(os.getcwd(), 'requirements.txt'),
}

Package = namedtuple('Package', [
    'editable', 'name_or_url', 'version', 'installed_version', 'etc',
])


class Requirements(object):
    patterns = OrderedDict([
        ('editable', '(?P<editable>-e )?'),
        ('name_or_url', '(?P<name_or_url>(?:(?!==|>|<|!=|~=).)+)'),
        ('version', '(?P<version>(?:==|>|<|!=|~=| )+[^\n;#\-]*\d)?'),
        ('etc', '(?P<etc>(?: +[#;\-]+[^\n]+)?\n?)'),
    ])

    def __init__(self, filepath):
        self.filepath = filepath
        self.buffer = ''

    def parse_package(self, package):
        pattern = '^{}$'.format(''.join(self.patterns.values()))
        match = re.search(pattern, package)
        editable, name_or_url, version, etc = match.groups()
        installed_version = self.get_installed_version(name_or_url)
        package = Package(
            bool(editable), name_or_url.strip(), version, installed_version,
            etc,
        )
        return package

    def make_line(self, package):
        line = package.name_or_url
        if package.editable:
            line = '-e ' + line

        if package.version:
            line += package.version
        elif package.installed_version:
            line += '~=' + package.installed_version

        if package.etc:
            line += package.etc

        return line

    def get_installed_version(self, package_name):
        try:
            return pkg_resources.get_distribution(package_name).version
        except (RequirementParseError, DistributionNotFound):
            return None

    def save_installed_packages(self, packages):
        self._read()

        for package in packages:
            package = self.parse_package(package)
            found = self._update_package(package)
            if not found:
                self._add_package(package)

        self._write()

    def _update_package(self, package):
        pattern = '^{}{}{}{}$'.format(
            self.patterns['editable'],
            re.escape(package.name_or_url),
            self.patterns['version'],
            self.patterns['etc'],
        )
        self.buffer, found = re.subn(
            pattern,
            '{}\g<etc>'.format(self.make_line(package)),
            self.buffer,
            flags=re.MULTILINE,
        )
        return found

    def _add_package(self, package):
        lines = self.buffer.split('\n')

        add_to_index = 0
        for i in range(len(lines)):
            line = lines[i].strip()

            # Add after firsts "-"
            if package.editable:
                if line.startswith('-'):
                    add_to_index = i + 1
                elif add_to_index:
                    break
                continue

            if not line or line.startswith(('#', '-')):
                continue

            buffer_package = self.parse_package(line)
            if buffer_package.name_or_url > package.name_or_url:
                break
            else:
                add_to_index = i + 1

        # Add after a multiline package
        while add_to_index and lines[add_to_index - 1].endswith('\\'):
            add_to_index += 1

        lines.insert(add_to_index, self.make_line(package))
        self.buffer = '\n'.join(lines)

    def _read(self):
        mode = 'r'
        if not os.path.exists(self.filepath):
            mode = 'w+'

        with open(self.filepath, mode) as f:
            self.buffer = f.read()

    def _write(self):
        with open(self.filepath, 'w+') as f:
            f.write(self.buffer)


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
@click.option('--save/--no-save', default=True)
def cli(pip_args, save):
    command = pip_args[0]
    pip_args = pip_args[1:]
    pip_output = subprocess.call(['pip', command] + list(pip_args))

    if pip_output != 0 or command not in ['install', 'uninstall'] or not save:
        return

    packages = []
    index_url = None
    extra_index_url = None
    find_links = None
    no_index = False

    pip_args = iter(pip_args)
    for arg in pip_args:
        if arg in ['-e', '--editable']:
            packages.append('-e ' + next(pip_args))

        if arg in ['-i', '--index-url']:
            index_url = next(pip_args)

        if arg == '--extra-index-url':
            extra_index_url = next(pip_args)

        if arg in ['-f', '--find-links']:
            find_links = next(pip_args)

        if arg == '--no-index':
            no_index = True

        if arg in ['-r', '--requirements']:
            next(pip_args)

        if arg.startswith('-'):
            continue

        packages.append(arg)

    if not packages:
        return

    req = Requirements(default_config['default_file'])
    req.save_installed_packages(packages)


def main():
    cli()


if __name__ == '__main__':
    sys.exit(main())
