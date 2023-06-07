import os
import pickle
import re
from typing import Union

import typer


def check_username(username: str) -> str:
    if not (len(username) >= 3 and len(username) <= 10):
        raise typer.BadParameter("Username must be between 3 and 10 characters")
    elif not username.isalnum():
        raise typer.BadParameter("Username must be alphanumeric; no other special chars allowed!")
    elif not username.islower():
        raise typer.BadParameter("Username must be lowercase")
    else:
        return username


def check_email(email: str) -> str:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email):
        return email
    else:
        raise typer.BadParameter("Give a valid email id")


def get_current_user() -> Union[dict, None]:
    if os.path.exists("current_user.pickle"):
        with open("current_user.pickle", "rb") as f:
            current_user = pickle.load(f)
            return current_user
    else:
        typer.secho("🚫 You are not logged in!", fg=typer.colors.RED)
        raise typer.Exit(1)
