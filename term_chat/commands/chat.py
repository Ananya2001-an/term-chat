import json
import os
import threading

import typer
from appwrite.exception import AppwriteException

from ..services.appwrite import database_id, dbs, rooms_collection_id
from ..utils.constants import spinner
from ..utils.room import get_input, get_room, show_messages
from ..utils.user import get_current_user

chat_app = typer.Typer()
current_room = {"messages": []}
stop_flag = threading.Event()


def subscribe(stop_flag) -> None:
    global current_room
    try:
        while not stop_flag.is_set():
            latest = dbs.get_document(database_id, rooms_collection_id, current_room["$id"])
            if latest["messages"] != current_room["messages"]:
                current_room = latest
                os.system("cls" if os.name == "nt" else "clear")
                show_messages(current_room)
    except AppwriteException as e:
        typer.secho(f"🚫 Error fetching document! '{e.message}' ", fg=typer.colors.RED)
        raise typer.Exit(1)


@chat_app.command()
def start():
    """Start chatting in a room :)"""
    current_user = get_current_user()
    room_name, room_admin_email = get_input()

    list_of_docs = get_room(room_admin_email, room_name)

    if list_of_docs["total"] == 0:
        typer.secho(
            f"🚫 Room with name {room_name} under admin {room_admin_email}" " does not exist!",
            fg=typer.colors.RED,
        )
    elif current_user["email"] not in list_of_docs["documents"][0]["members"]:
        typer.secho(
            "🚫 You are not a member! Join first using command: room join",
            fg=typer.colors.RED,
        )
    else:
        spinner("Opening chat room...", 2)
        global current_room
        global stop_flag
        current_room = list_of_docs["documents"][0]
        background_thread = threading.Thread(target=subscribe, args=(stop_flag,))
        # Set the thread as a daemon so it runs in the background
        background_thread.daemon = True
        # Start the thread
        background_thread.start()
        show_messages(current_room)
        while True:
            message = typer.prompt("")
            if message == "exit":
                typer.secho("Come again...👋", fg=typer.colors.GREEN)
                stop_flag.set()
                # Wait for the background thread to complete
                background_thread.join()
                exit(0)
            else:
                current_room["messages"].append(
                    json.dumps(
                        {
                            "id": current_user["email"],
                            "username": current_user["name"],
                            "message": message,
                        }
                    )
                )
                updated_messages = {"messages": current_room["messages"]}
                try:
                    dbs.update_document(
                        database_id, rooms_collection_id, current_room["$id"], updated_messages
                    )
                except AppwriteException as e:
                    typer.secho(
                        f"🚫 Error sending message! Try again. '{e.message}' ", fg=typer.colors.RED
                    )
