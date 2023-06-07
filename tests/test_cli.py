import pytest
from typer.testing import CliRunner

from term_chat.__main__ import app


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_create_user(runner):
    result = runner.invoke(app, ["auth", "create-user"], input="testuser\ntest@gmail.com\n")
    assert result.exit_code == 0
    assert "🦄 Account created successfully for user: testuser '<test@gmail.com>'!" in result.stdout


def test_login(runner):
    result = runner.invoke(app, ["auth", "login"], input="test@gmail.com\n")
    assert result.exit_code == 0
    assert "🦄 You are accessing the account of: testuser" in result.stdout


def test_whoami(runner):
    result = runner.invoke(app, ["auth", "whoami"])
    assert result.exit_code == 0
    assert "🦄 You are logged in as: testuser" in result.stdout


def test_create_room(runner):
    result = runner.invoke(app, ["room", "create"], input="test room\ntest description\ntestid")
    assert result.exit_code == 0
    assert "🦄 Created room test room successfully!" in result.stdout


def test_list_all(runner):
    result = runner.invoke(app, ["room", "list-all"])
    assert result.exit_code == 0
    assert "🦄 Your rooms:" in result.stdout


def test_info(runner):
    result = runner.invoke(app, ["room", "info"], input="test room\ntestid\n")
    assert result.exit_code == 0
    assert "🦄 Info about room test room with id testid:" in result.stdout


def test_delete_room(runner):
    result = runner.invoke(app, ["room", "delete"], input="test room\n")
    assert result.exit_code == 0
    assert "🦄 Deleted room test room successfully!" in result.stdout


def test_delete_user(runner):
    result = runner.invoke(app, ["auth", "delete-user"])
    assert result.exit_code == 0
    assert "🦄 User testuser deleted successfully!" in result.stdout
