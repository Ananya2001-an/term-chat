import json
from typing import Union

import typer
from appwrite.exception import AppwriteException
from appwrite.query import Query

from ..services.appwrite import database_id, dbs, rooms_collection_id
from ..utils.constants import console, error_style, header_style, message_style, success_style
from ..utils.user import get_current_user


def get_input() -> list:
    room_name = typer.prompt("Enter room name")
    room_admin_email = typer.prompt("Enter room admin's email id")

    return [room_name, room_admin_email]


def get_room(admin_email: str, name: str = None) -> Union[dict, None]:
    try:
        list_of_docs = dbs.list_documents(
            database_id,
            rooms_collection_id,
            [Query.equal("name", name), Query.equal("admin_email", admin_email)]
            if name
            else [Query.equal("admin_email", admin_email)],
        )
        return list_of_docs
    except AppwriteException as e:
        console.print(f"🚫 DB query error! '{e.message}' ", style=error_style)
        raise typer.Exit(1)


def show_messages(room: dict) -> None:
    current_user = get_current_user()
    console.print(f"🦄 Welcome to {room['name']}!", style=header_style)
    console.print(f"👉 Admin: {room['admin']} <'{room['admin_email']}'>", style=success_style)
    console.print(f"👉 Members: {', '.join(room['members'])}", style=success_style)
    console.print("👉 Messages:", style=success_style)
    for message in room["messages"]:
        msg_dict = json.loads(message)
        console.print(
            f"👉 {msg_dict['username'] if msg_dict['username'] != current_user['name'] else 'You'}"
            f": {msg_dict['message']}",
            style=(message_style if msg_dict["username"] != current_user["name"] else header_style),
        )
    console.print("👉 Enter your message below:(type 'exit' to leave)", style=success_style)
