from click.testing import CliRunner

from pipw.main import cli


def invoke_cli(commands, config_file):
    if isinstance(commands, str):
        commands = commands.split()
    runner = CliRunner()
    commands += ['--config', config_file.strpath]
    return runner.invoke(cli, commands)


def check_requirements_snapshot(tmpdir, snapshot, requirements_path=None):
    if not requirements_path:
        requirements_path = tmpdir.join('requirements.txt')
    output = requirements_path.read()
    snapshot.assert_match(output)
