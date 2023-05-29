#!/usr/bin/env python
""" Term-Chat is a console chat application """

import typer

from .commands.auth import auth_app
from .commands.room import room_app

app = typer.Typer()
app.add_typer(auth_app, name="auth")
app.add_typer(room_app, name="room")

if __name__ == "__main__":
    app()
