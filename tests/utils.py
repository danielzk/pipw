from click.testing import CliRunner

from pipw.main import cli


def invoke_cli(commands, config_file):
    if isinstance(commands, str):
        commands = commands.split()
    runner = CliRunner()
    commands += ['--config', config_file.strpath]
    runner.invoke(cli, commands)
