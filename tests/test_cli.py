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
        result = runner.invoke(app, ["auth", "create-user", "testuser", "test@gmail.com"])
        assert result.exit_code == 0
        assert "🦄 Account created successfully for user: test@gmail.com!" in result.stdout

    def test_login(self, runner):
        result = runner.invoke(app, ["auth", "login", "test@gmail.com"])
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

    def test_logout(self, runner):
        runner.invoke(app, ["auth", "login", "abc@gmail.com"])
        result = runner.invoke(app, ["auth", "logout"])
        assert result.exit_code == 0
        assert "🦄 You have been logged out successfully!" in result.stdout


class TestRoomCommands:
    def test_create(self, runner):
        runner.invoke(app, ["auth", "login", "xyz@gmail.com"])
        result = runner.invoke(app, ["room", "create"], input="test room\ntest description\n")
        assert result.exit_code == 0
        assert "🦄 Created room test room successfully!" in result.stdout

    def test_list_all(self, runner):
        result = runner.invoke(app, ["room", "list-all"])
        assert result.exit_code == 0
        assert "🦄 Your rooms:" in result.stdout

    def test_info(self, runner):
        result = runner.invoke(app, ["room", "info"], input="test room\nxyz@gmail.com\n")
        assert result.exit_code == 0
        assert "🦄 Info about room test room under admin xyz@gmail.com:" in result.stdout

    def test_join(self, runner):
        result = runner.invoke(app, ["room", "join"], input="room1\nabc@gmail.com")
        assert result.exit_code == 0
        assert "🦄 Joined room room1 under admin abc@gmail.com" " successfully!" in result.stdout

    def test_leave(self, runner):
        result = runner.invoke(app, ["room", "leave"], input="room1\nabc@gmail.com")
        assert result.exit_code == 0
        assert "🦄 Left room room1 under admin abc@gmail.com" " successfully!"

    def test_delete(self, runner):
        result = runner.invoke(app, ["room", "delete"], input="test room\n")
        assert result.exit_code == 0
        assert "🦄 Deleted room test room successfully!" in result.stdout
        runner.invoke(app, ["auth", "logout"])
