import typer
import os
import pickle
import time
from ..services.appwrite import users
from ..utils.constants import error_style, success_style, console, spinner
from ..utils.user import check_email, check_username

from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.query import Query
from typing_extensions import Annotated

auth_app = typer.Typer()


@auth_app.command()
def create_user(
    username: Annotated[
        str,
        typer.Argument(
            help="username must be lowercase, alphanumeric, and between 3 to 10 characters",
            callback=check_username,
        ),
    ],
    email: Annotated[
        str,
        typer.Argument(help="give a valid email id", callback=check_email),
    ],
):
    """Create a new user on term-chat"""
    spinner("Creating user...", 2)
    try:
        users.create(user_id=ID.unique(), email=email, name=username)
        console.print(
            f"🦄 Account created successfully for user: {email}! Please login to continue.",
            style=success_style,
        )
    except AppwriteException as e:
        if e.message.startswith("A user with the same email"):
            console.print("🚫 A user with the same email already exists!", style=error_style)
        else:
            console.print(
                "🚫 Sorry! There was an error creating your account. Please try again later.",
                style=error_style,
            )


@auth_app.command()
def login(
    email: Annotated[
        str,
        typer.Argument(help="give a valid email id", callback=check_email),
    ]
):
    """Login to an existing user account"""
    if not os.path.exists("current_user.pickle"):
        spinner("Logging in...", 2)
        try:
            list_of_users = users.list(queries=[Query.equal("email", [email])])
            if list_of_users["total"] == 0:
                console.print("🚫 No users found! Please create an account first.", style=error_style)
            else:
                current_user = list_of_users["users"][0]
                with open("current_user.pickle", "wb") as file:
                    pickle.dump(current_user, file)
                console.print(
                    f"🦄 You are accessing the account of: {current_user['name']}", style=success_style
                )
        except AppwriteException:
            console.print(
                "🚫 Error fetching user with the given input credentials! Try again.", style=error_style
            )
    else:
        console.print("🚫 You are already logged in!", style=error_style)


@auth_app.command()
def logout():
    """Logout the current user"""
    if os.path.exists("current_user.pickle"):
        os.remove("current_user.pickle")
        console.print("🦄 You have been logged out successfully!", style=success_style)
    else:
        console.print("🚫 You are not logged in!", style=error_style)
