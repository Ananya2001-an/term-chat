import json
from typing import Optional

import typer
from appwrite.exception import AppwriteException
from appwrite.query import Query

from ..services.appwrite import database_id, dbs, rooms_collection_id
from ..utils.user import get_current_user


def check_room_id(room_id: str) -> None:
    if not (room_id.isalnum() and len(room_id) <= 15):
        typer.secho("🚫 Room id must be alphanumeric and less than 15 characters!", fg=typer.colors.RED)
        raise typer.Exit(1)
    elif (
        dbs.list_documents(
            database_id,
            rooms_collection_id,
            [Query.equal("room_id", room_id)],
        )["total"]
        != 0
    ):
        typer.secho(f"🚫 Room with id {room_id} is already taken!", fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        return None


def get_input() -> list[str]:
    room_name = typer.prompt("Enter room name")
    room_id = typer.prompt("Enter room id")

    return [room_name, room_id]


def get_room(room_id: str, name: str) -> Optional[dict]:
    try:
        list_of_docs = dbs.list_documents(
            database_id,
            rooms_collection_id,
            [Query.equal("name", name), Query.equal("room_id", room_id)],
        )
        return list_of_docs
    except AppwriteException as e:
        typer.secho(f"🚫 DB query error! '{e.message}' ", fg=typer.colors.RED)
        raise typer.Exit(1)


def show_messages(room: dict) -> None:
    current_user = get_current_user()
    typer.secho(f"🦄 Welcome to {room['name']}!", fg=typer.colors.MAGENTA)
    typer.secho(f"👉 Admin: {room['admin']} <'{room['admin_email']}'>", fg=typer.colors.GREEN)
    typer.secho(f"👉 Members: {', '.join(room['members'])}", fg=typer.colors.GREEN)
    typer.secho("👉 Messages:", fg=typer.colors.GREEN)
    for message in room["messages"]:
        msg_dict = json.loads(message)
        typer.secho(
            f"👉 {msg_dict['username'] if msg_dict['username'] != current_user['name'] else 'You'}"
            f": {msg_dict['message']}",
            fg=(
                typer.colors.CYAN
                if msg_dict["username"] != current_user["name"]
                else typer.colors.MAGENTA
            ),
        )
    typer.secho("👉 Enter your message below:(type 'exit' to leave)", fg=typer.colors.GREEN)
