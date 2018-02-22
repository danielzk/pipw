from click.testing import CliRunner
from pkg_resources import DistributionNotFound

from pipw.main import cli


def invoke_cli(commands, config_file, print_output=False):
    if isinstance(commands, str):
        commands = commands.split()

    commands += ['--config', config_file.strpath]
    runner = CliRunner()
    result = runner.invoke(cli, commands)

    if result.output and print_output:
        print(result.output)

    if result.exception and print_output:
        raise result.exception

    return result


def check_requirements_snapshot(tmpdir, snapshot, requirements_path=None):
    if not requirements_path:
        requirements_path = tmpdir.join('requirements.txt')
    output = requirements_path.read()
    snapshot.assert_match(output)
