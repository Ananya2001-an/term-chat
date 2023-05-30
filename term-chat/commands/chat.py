import typer
import json
import threading
import os
from ..utils.constants import (
    console,
    error_style,
    success_style,
    message_style,
    header_style,
    spinner,
)
from ..utils.user import get_current_user
from ..utils.room import get_room, get_input, show_messages
from ..services.appwrite import dbs, database_id, rooms_collection_id
from appwrite.exception import AppwriteException

chat_app = typer.Typer()
current_room = {"messages": []}
stop_flag = threading.Event()


def subscribe() -> None:
    global current_room
    try:
        while not stop_flag.is_set():
            latest = dbs.get_document(database_id, rooms_collection_id, current_room["$id"])
            if latest["messages"] != current_room["messages"]:
                current_room = latest
                os.system("cls" if os.name == "nt" else "clear")
                show_messages(current_room)
    except AppwriteException as e:
        console.print(f"🚫 Error fetching document! '{e.message}' ", style=error_style)
        raise typer.Exit(1)


@chat_app.command()
def start():
    """Start chatting in a room :)"""
    current_user = get_current_user()
    room_name, room_admin_email = get_input()

    list_of_docs = get_room(room_admin_email, room_name)

    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} under admin {room_admin_email}" " does not exist!",
            style=error_style,
        )
    elif current_user["email"] not in list_of_docs["documents"][0]["members"]:
        console.print(
            f"🚫 You are not a member! Join first using command: room join",
            style=error_style,
        )
    else:
        spinner("Opening chat room...", 2)
        global current_room
        current_room = list_of_docs["documents"][0]
        background_thread = threading.Thread(target=subscribe)
        # Set the thread as a daemon so it runs in the background
        background_thread.daemon = True
        # Start the thread
        background_thread.start()
        show_messages(current_room)
        while True:
            message = typer.prompt("")
            if message == "exit":
                console.print(f"Come again...👋", style=success_style)
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
                    console.print(
                        f"🚫 Error sending message! Try again. '{e.message}' ", style=error_style
                    )
