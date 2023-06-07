import os
import pickle

import typer
from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.query import Query

from ..services.appwrite import users
from ..utils.constants import spinner
from ..utils.user import check_email, check_username, get_current_user

auth_app = typer.Typer()


@auth_app.command()
def create_user():
    """Create a new user on term-chat"""
    username: str = typer.prompt("Enter a username for your term-chat account")
    check_username(username)
    email: str = typer.prompt("Enter your email id")
    check_email(email)

    spinner("Creating user...", 2)
    try:
        users.create(user_id=ID.unique(), name=username, email=email)
        typer.secho(
            f"🦄 Account created successfully for user: {username} '<{email}>'!"
            "Please login to continue.",
            fg=typer.colors.GREEN,
        )
    except AppwriteException as e:
        if e.message.startswith("A user with the same email"):
            typer.secho("🚫 A user with the same email already exists!", fg=typer.colors.RED)
        else:
            typer.secho(
                "🚫 Sorry! There was an error creating your account. Please try again later.",
                fg=typer.colors.RED,
            )


@auth_app.command()
def login():
    """Login to an existing user account"""
    email: str = typer.prompt("Enter your email id")
    check_email(email)

    if not os.path.exists("current_user.pickle"):
        spinner("Logging in...", 2)
        try:
            list_of_users = users.list(queries=[Query.equal("email", [email])])
            if list_of_users["total"] == 0:
                typer.secho("🚫 No users found! Please create an account first.", fg=typer.colors.RED)
            else:
                current_user = list_of_users["users"][0]
                with open("current_user.pickle", "wb") as file:
                    pickle.dump(current_user, file)
                typer.secho(
                    f"🦄 You are accessing the account of: {current_user['name']}", fg=typer.colors.GREEN
                )
        except AppwriteException as e:
            typer.secho(
                f"🚫 Error fetching user with the given input credentials! Try again. {e}",
                fg=typer.colors.RED,
            )
    else:
        typer.secho("🚫 You are already logged in!", fg=typer.colors.RED)


@auth_app.command()
def logout():
    """Logout the current user"""
    if os.path.exists("current_user.pickle"):
        os.remove("current_user.pickle")
        typer.secho("🦄 You have been logged out successfully!", fg=typer.colors.GREEN)
    else:
        typer.secho("🚫 You are not logged in!", fg=typer.colors.RED)


@auth_app.command()
def whoami():
    """Check the current user"""
    current_user = get_current_user()
    typer.secho(f"🦄 You are logged in as: {current_user['name']}", fg=typer.colors.GREEN)


@auth_app.command()
def delete_user():
    """Delete the current user"""
    current_user = get_current_user()
    spinner("Deleting user...", 2)
    try:
        users.delete(current_user["$id"])
        typer.secho(f"🦄 User {current_user['name']} deleted successfully!", fg=typer.colors.GREEN)
        os.remove("current_user.pickle")
    except AppwriteException:
        typer.secho("🚫 Error deleting user! Try again.", fg=typer.colors.RED)
