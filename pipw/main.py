from collections import namedtuple, OrderedDict
import os
from os.path import dirname
import pkg_resources
from pkg_resources import RequirementParseError, DistributionNotFound
import re
import sys
import subprocess

import click
import yaml

PIP_OPTIONS = {
    'editable': ['-e', '--editable'],
    'index_url': ['-i', '--index-url'],
    'extra_index_url': ['--extra-index-url'],
    'find_links': ['-f', '--find-links'],
    'no_index': ['--no-index'],
    'requirements': ['-r', '--requirements'],
}

Package = namedtuple('Package', [
    'editable', 'name_or_url', 'version', 'installed_version', 'etc',
])


class Requirements(object):
    patterns = OrderedDict([
        ('editable', '(?P<editable>-e )?'),
        ('name_or_url', '(?P<name_or_url>(?:(?!==|>|<|>=|<=|!=|~=).)+)'),
        ('version', '(?P<version>(?: *(?:==|>|<|>=|<=|!=|~=) *[^\n ]+)+)?'),
        ('etc', '(?P<etc>(?: +[#;\-]+[^\n]+)?\n?)'),
    ])

    def __init__(self, config, filepath):
        self.config = config
        self.filepath = filepath
        self.buffer = None

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
            line += self.config['specifier'] + package.installed_version

        if package.etc:
            line += package.etc

        return line

    def get_installed_version(self, package_name):
        try:
            return pkg_resources.get_distribution(package_name).version
        except (RequirementParseError, DistributionNotFound):
            return None

    def save_installed_packages(self, packages):
        if self.buffer is None:
            self.read()

        for package in packages:
            package = self.parse_package(package)
            found = self._update_package(package)
            if not found:
                self._add_package(package)

    def save_extra_index_urls(self, urls):
        if self.buffer is None:
            self.read()

        option = 'extra_index_url'
        for url in urls:
            found = self._search_option(option, url)
            if not found:
                self._add_option(option, url)

    def save_index_url(self, url):
        if self.buffer is None:
            self.read()

        option = 'index_url'
        found = self._update_option(option, url)
        if not found:
            self._add_option(option, url)

    def save_no_index(self):
        if self.buffer is None:
            self.read()

        option = 'no_index'
        found = self._search_option(option)
        if not found:
            self._add_option(option)

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

            # Add after first "-" group
            if package.editable:
                if line.startswith('-'):
                    add_to_index = i + 1
                elif add_to_index:
                    break
                continue

            if not line or line.startswith(('#', '-')):
                if line.startswith('-') and not add_to_index:
                    add_to_index = i + 1
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

    def _search_option(self, option, value=''):
        if value:
            value = ' {}'.format(value)

        pattern = '^(?:{}){}{}$'.format(
            '|'.join(PIP_OPTIONS[option]),
            value,
            self.patterns['etc'],
        )
        return re.search(pattern, self.buffer, flags=re.MULTILINE)

    def _update_option(self, option, value):
        pattern = '^(?P<option>{}) [^ ]+{}$'.format(
            '|'.join(PIP_OPTIONS[option]),
            self.patterns['etc'],
        )
        self.buffer, found = re.subn(
            pattern,
            '\g<option> {}\g<etc>'.format(value),
            self.buffer,
            flags=re.MULTILINE,
        )
        return found

    def _add_option(self, option, value=''):
        lines = self.buffer.split('\n')

        add_to_index = 0
        lines_indices = iter(range(len(lines)))
        for i in lines_indices:
            line = lines[i].strip()
            if line.startswith('-'):
                add_to_index = i + 1
                while lines[add_to_index - 1].endswith('\\'):
                    add_to_index += 1
                    next(lines_indices)
                break

        new_line = '{} {}'.format(PIP_OPTIONS[option][0], value).strip()
        lines.insert(add_to_index, new_line)
        self.buffer = '\n'.join(lines)

    def read(self):
        filedir = dirname(self.filepath)
        if filedir and not os.path.exists(filedir):
            os.makedirs(filedir)

        mode = 'r'
        if not os.path.exists(self.filepath):
            mode = 'w+'

        with open(self.filepath, mode) as stream:
            self.buffer = stream.read()

    def write(self):
        with open(self.filepath, 'w+') as stream:
            stream.write(self.buffer)


def init_config(config_path=None):
    config = {
        'requirements': 'requirements.txt',
        'specifier': '~=',
    }

    filepath = '.pipwrc'
    if config_path:
        filepath = config_path

    if os.path.exists(filepath):
        with open(filepath, 'r') as stream:
            custom_config = yaml.safe_load(stream)
            if not isinstance(custom_config, dict):
                exit('Invalid .pipwrc')
            config.update(custom_config)
    elif config_path:
        exit('Config file "{}" not found'.format(config_path))

    return config


help = {
    'save': (
        'Save packages to the requirements file. This is default unless '
        '--no-save. Packages are saved in requirements.txt unless a custom '
        'configuration is used.'
    ),
    'no_save': 'Prevent save packages to the requirements file.',
    'config': (
        'Pass a custom config file. By default it looks for a .pipwrc '
        'file in the directory where the command is executed.'
    ),
}

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
@click.option('--save', '-s', help=help['save'], is_flag=True)
@click.option('--no-save', '-n', help=help['no_save'], is_flag=True)
@click.option('--config', '-c', help=help['config'], metavar='<path>')
def cli(pip_args, save, no_save, config):
    if save and no_save:
        exit('--save and --no-save options are mutually exclusive')

    save = not no_save
    config = init_config(config)
    command = pip_args[0]
    pip_args = pip_args[1:]
    pip_output = subprocess.call(['pip', command] + list(pip_args))

    if pip_output != 0 or command not in ['install', 'uninstall'] or not save:
        return

    packages = []
    index_url = None
    extra_index_urls = None
    find_links = None
    no_index = False

    pip_args = iter(pip_args)
    for arg in pip_args:
        if arg in PIP_OPTIONS['editable']:
            packages.append('-e ' + next(pip_args))
        elif arg in PIP_OPTIONS['index_url']:
            index_url = next(pip_args)
        elif arg in PIP_OPTIONS['extra_index_url']:
            extra_index_urls = next(pip_args).split(',')
        elif arg in PIP_OPTIONS['find_links']:
            find_links = next(pip_args)
        elif arg in PIP_OPTIONS['no_index']:
            no_index = True
        elif arg in PIP_OPTIONS['requirements']:
            # Skip requirements argument
            next(pip_args)

        if arg.startswith('-'):
            continue

        packages.append(arg)

    if not packages:
        return

    req = Requirements(config, config['requirements'])
    req.save_installed_packages(packages)

    if index_url:
        req.save_index_url(index_url)

    if extra_index_urls:
        req.save_extra_index_urls(extra_index_urls)

    if no_index:
        req.save_no_index()

    req.write()


if __name__ == '__main__':
    sys.exit(cli())
