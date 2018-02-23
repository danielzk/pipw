from collections import namedtuple, OrderedDict
import os
from os.path import dirname
import re
import sys

import click
import pip
import pkg_resources
from pkg_resources import RequirementParseError, DistributionNotFound
import yaml

PIP_OPTIONS = {
    'editable': ['-e', '--editable'],
    'index_url': ['-i', '--index-url'],
    'extra_index_url': ['--extra-index-url'],
    'find_links': ['-f', '--find-links'],
    'no_index': ['--no-index'],
    'requirements': ['-r', '--requirements'],
    'install_option': ['--install-option'],
    'global_option': ['--global-option'],
}

CLI_HELP = {
    'save': (
        'Save packages to the requirements file. This is default unless '
        '--no-save. Packages are saved in requirements.txt unless a custom '
        'configuration is used.'
    ),
    'no_save': 'Prevent save packages to the requirements file.',
    'config': (
        'Pass a custom config file. By default it looks for a .pipwrc '
        'file in the directory where the command is executed, or in the '
        "user's home directory."
    ),
    'env': 'Save in a environment previously declared in the config file.',
    'save_to': 'Save to a custom file.',
    'no_detect_version': (
        'Do not detect installed version, and save package version only if '
        'the version is passed.'
    ),
}

Package = namedtuple('Package', [
    'editable', 'name_or_url', 'version', 'installed_version', 'options',
])


# pylint: disable=anomalous-backslash-in-string
class Requirements(object):
    patterns = OrderedDict([
        ('editable', '(?P<editable>-e )?'),
        ('name_or_url', '(?P<name_or_url>(?:(?!==|>|<|>=|<=|!=|~=| #| -).)+)'),
        ('version', '(?P<version>(?: *(?:==|>|<|>=|<=|!=|~=) *[^\n ]+)+)?'),
        ('options', '(?P<options>(?: +\-+[^#\n ]+)*\n?)'),
        ('comment', '(?P<comment>(?: +#[^\n]+)?\n?)'),
    ])

    def __init__(self, config, filepath):
        self.config = config
        self.filepath = filepath
        self.buffer = None

    def parse_package(self, package):
        pattern = '^{}$'.format(''.join(self.patterns.values()))
        match = re.search(pattern, package)
        if not match:
            return None

        editable, name_or_url, version, options, comment = match.groups()
        options = options.split()

        installed_version = None
        if self.config['detect_version']:
            installed_version = self.get_installed_version(name_or_url)

        package = Package(
            bool(editable), name_or_url.strip(), version, installed_version,
            options,
        )
        return package

    def make_line(self, package):
        line = package.name_or_url
        if package.editable:
            line = '-e ' + line

        if package.version:
            line += package.version
        elif self.config['detect_version'] and package.installed_version:
            line += self.config['specifier'] + package.installed_version

        if package.options:
            options = ' '.join(package.options)
            line += ' {}'.format(options)

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
            found = self._update_package(package)
            if not found:
                self._add_package(package)

    def save_option(self, option, values=None):
        if self.buffer is None:
            self.read()

        if not isinstance(values, list):
            values = [values]

        for value in values:
            # An option can be updated if appear only once and have a value
            if option == 'index_url':
                found = self._update_option(option, value)
            else:
                found = self._search_option(option, value)

            if not found:
                self._add_option(option, value)

    def remove_packages(self, packages):
        if self.buffer is None:
            self.read()

        for package in packages:
            self._remove_package(package)

    def _update_package(self, package):
        lines = self.buffer.split('\n')

        found = False
        for i, line in enumerate(lines):
            line = line.strip()

            # Concatenate multiline
            next_line_index = i + 1
            while line.endswith('\\'):
                line += lines[next_line_index]
                next_line_index += 1
            line = line.replace('\\', ' ')

            buffer_package = self.parse_package(line)
            if (not buffer_package or
                    buffer_package.name_or_url.lower() !=
                    package.name_or_url.lower()):
                continue

            found = True
            package.options.extend(buffer_package.options)
            new_line = self.make_line(package)

            comment_start = ' #'
            if comment_start in line:
                comment = line.split(comment_start, 1)[1]
                new_line += comment_start + comment

            # Remove multiline
            line = lines[i].strip()
            while line.endswith('\\'):
                line += lines[i + 1]
                del lines[i + 1]

            lines[i] = new_line
            break

        self.buffer = '\n'.join(lines)
        return found

    def _add_package(self, package):
        lines = self.buffer.split('\n')

        add_to_index = 0
        for i, line in enumerate(lines):
            line = line.strip()

            # If is an empty line, a comment or multiline continuation
            if (not line or
                    line.startswith('#') or
                    (i and lines[i - 1].endswith('\\'))):
                continue

            if line.startswith('-'):
                add_to_index = i + 1
                continue

            if package.editable:
                continue

            buffer_package = self.parse_package(line)
            if buffer_package.name_or_url > package.name_or_url:
                break
            else:
                add_to_index = i + 1

        while add_to_index and lines[add_to_index - 1].endswith('\\'):
            add_to_index += 1

        lines.insert(add_to_index, self.make_line(package))
        self.buffer = '\n'.join(lines)

    def _remove_package(self, package):
        lines = self.buffer.split('\n')
        for i, line in enumerate(lines):
            next_line_index = i + 1
            while line.endswith('\\'):
                line += lines[next_line_index]
                next_line_index += 1
            line = line.replace('\\', ' ')

            buffer_package = self.parse_package(line)
            if (not buffer_package or
                    buffer_package.name_or_url.lower() !=
                    package.name_or_url.lower()):
                continue

            line = lines[i]
            while line.endswith('\\'):
                line += lines[i + 1]
                del lines[i + 1]
            del lines[i]

            self.buffer = '\n'.join(lines)
            break

    def _search_option(self, option, value=None):
        value_pattern = ''
        if value:
            value_pattern = ' {}'.format(value)

        pattern = '^(?:{}){}{}$'.format(
            '|'.join(PIP_OPTIONS[option]),
            value_pattern,
            self.patterns['comment'],
        )
        return re.search(pattern, self.buffer, flags=re.MULTILINE)

    def _update_option(self, option, value):
        pattern = '^(?P<option>{}) [^ ]+{}$'.format(
            '|'.join(PIP_OPTIONS[option]),
            self.patterns['comment'],
        )
        self.buffer, found = re.subn(
            pattern,
            '\g<option> {}\g<comment>'.format(value),
            self.buffer,
            flags=re.MULTILINE,
        )
        return found

    def _add_option(self, option, value=None):
        lines = self.buffer.split('\n')

        add_to_index = 0
        for i, line in enumerate(lines):
            line = line.strip()

            if line.startswith(('-e ', '--editable')):
                add_to_index = i
                break

            if i and lines[i - 1].endswith('\\'):
                continue

            if line.startswith('-'):
                add_to_index = i + 1

        while add_to_index and lines[add_to_index - 1].endswith('\\'):
            add_to_index += 1

        if not value:
            value = ''

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


def init_config(config_path=None, json_config=None):
    config = {
        'requirements': 'requirements.txt',
        'specifier': '~=',
        'detect_version': True,
        'envs': {},
    }

    filepath = '.pipwrc'
    if not os.path.exists(filepath):
        home = os.path.expanduser('~')
        filepath = os.path.join(home, filepath)

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

    def is_true(value):
        return str(value).lower() in ['y', 'yes', 'true', 'on']

    config.update(json_config)
    config['detect_version'] = is_true(config['detect_version'])
    return config


# pylint: disable=no-value-for-parameter
@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('pip_args', nargs=-1, type=click.UNPROCESSED)
@click.option('--save', '-s', help=CLI_HELP['save'], is_flag=True)
@click.option('--no-save', '-n', help=CLI_HELP['no_save'], is_flag=True)
@click.option('--config', help=CLI_HELP['config'], metavar='<path>')
@click.option('--env', '-m', help=CLI_HELP['env'], metavar='<name>')
@click.option('--save-to', help=CLI_HELP['save_to'], metavar='<path>')
@click.option(
    '--no-detect-version', default=False, help=CLI_HELP['no_detect_version'],
    is_flag=True,
)
def cli(pip_args, save, no_save, config, env, save_to, no_detect_version):
    if save and no_save:
        exit('--save and --no-save options are mutually exclusive')

    if env and save_to:
        exit('--env and --save-to options are mutually exclusive')

    json_config = {}
    if no_detect_version:
        json_config['detect_version'] = False
    config = init_config(config, json_config)

    requirements_file = config['requirements']
    if env:
        if env not in config['envs']:
            exit('Environmment "{}" not found'.format(env))
        requirements_file = config['envs'][env]
    elif save_to:
        requirements_file = save_to

    # Call pip
    pip_output = pip.main(list(pip_args))

    command = pip_args[0]
    pip_args = pip_args[1:]
    save = not no_save

    if pip_output != 0 or command not in ['install', 'uninstall'] or not save:
        return

    req = Requirements(config, requirements_file)

    packages = []
    install_options = []
    global_options = []
    pip_args = iter(pip_args)
    for arg in pip_args:
        if arg in PIP_OPTIONS['editable']:
            line = '-e ' + next(pip_args)
            packages.append(req.parse_package(line))
        elif arg in PIP_OPTIONS['index_url']:
            url = next(pip_args)
            req.save_option('index_url', url)
        elif arg in PIP_OPTIONS['extra_index_url']:
            urls = next(pip_args).split(',')
            req.save_option('extra_index_url', urls)
        elif arg in PIP_OPTIONS['find_links']:
            url = next(pip_args)
            req.save_option('find_links', url)
        elif arg in PIP_OPTIONS['no_index']:
            req.save_option('no_index')
        elif arg in PIP_OPTIONS['requirements']:
            # Skip requirements argument
            next(pip_args)
        elif arg in PIP_OPTIONS['install_option']:
            install_options.append(next(pip_args))
        elif arg in PIP_OPTIONS['global_option']:
            global_options.append(next(pip_args))

        if arg.startswith('-'):
            continue

        packages.append(req.parse_package(arg))

    if not packages:
        return

    if install_options or global_options:
        for package in packages:
            for value in install_options:
                package.options.append('--install-option=' + value)
            for value in global_options:
                package.options.append('--global-option=' + value)

    if command == 'install':
        req.save_installed_packages(packages)
    elif env or save_to:
        req.remove_packages(packages)
    else:
        # Remove for all environments
        req = Requirements(config, config['requirements'])
        req.remove_packages(packages)
        for file_ in config['envs'].values():
            env_req = Requirements(config, file_)
            env_req.remove_packages(packages)
            env_req.write()

    req.write()


if __name__ == '__main__':
    sys.exit(cli())
