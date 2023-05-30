import pytest
import importlib
from typer.testing import CliRunner

module = importlib.import_module("term-chat.__main__")
app = module.app

@pytest.fixture(scope="module")
def runner():
    return CliRunner()


class TestAuthCommands:

    def test_login(self, runner):
        result = runner.invoke(app, ["auth", "login", "abc@gmail.com"])
        assert result.exit_code == 0
        assert "🦄 You are accessing the account of: user1" in result.stdout

    def test_whoami(self, runner):
        result = runner.invoke(app, ["auth", "whoami"])
        assert result.exit_code == 0
        assert "🦄 You are logged in as: user1" in result.stdout
    
    def test_logout(self, runner):
        result = runner.invoke(app, ["auth", "logout"])
        assert result.exit_code == 0
        assert "🦄 You have been logged out successfully!" in result.stdout
