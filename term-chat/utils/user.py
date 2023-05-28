import typer
import re


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
