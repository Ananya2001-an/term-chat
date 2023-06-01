import importlib

import pytest
from typer.testing import CliRunner

module = importlib.import_module("term_chat.__main__")
app = module.app


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


class TestAuthCommands:
    def test_create_user(self, runner):
        result = runner.invoke(app, ["auth", "create-user"], input="testuser\ntest@gmail.com\n")
        assert result.exit_code == 0
        assert "🦄 Account created successfully for user: testuser '<test@gmail.com>'!" in result.stdout

    def test_login(self, runner):
        result = runner.invoke(app, ["auth", "login"], input="test@gmail.com\n")
        assert result.exit_code == 0
        assert "🦄 You are accessing the account of: testuser" in result.stdout

    def test_whoami(self, runner):
        result = runner.invoke(app, ["auth", "whoami"])
        assert result.exit_code == 0
        assert "🦄 You are logged in as: testuser" in result.stdout

    def test_delete_user(self, runner):
        result = runner.invoke(app, ["auth", "delete-user"])
        assert result.exit_code == 0
        assert "🦄 User testuser deleted successfully!" in result.stdout


class TestRoomCommands:
    def test_create(self, runner):
        runner.invoke(app, ["auth", "create-user"], input="testuser\ntest@gmail.com\n")
        runner.invoke(app, ["auth", "login"], input="test@gmail.com\n")
        result = runner.invoke(app, ["room", "create"], input="test room\ntest description\ntestid")
        assert result.exit_code == 0
        assert "🦄 Created room test room successfully!" in result.stdout

    def test_list_all(self, runner):
        result = runner.invoke(app, ["room", "list-all"])
        assert result.exit_code == 0
        assert "🦄 Your rooms:" in result.stdout

    def test_info(self, runner):
        result = runner.invoke(app, ["room", "info"], input="test room\ntestid\n")
        assert result.exit_code == 0
        assert "🦄 Info about room test room with id testid:" in result.stdout

    def test_delete(self, runner):
        result = runner.invoke(app, ["room", "delete"], input="test room\n")
        assert result.exit_code == 0
        assert "🦄 Deleted room test room successfully!" in result.stdout
        runner.invoke(app, ["auth", "delete-user"])
