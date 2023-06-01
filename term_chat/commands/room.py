import json

import typer
from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.query import Query
from prettytable.colortable import ColorTable, Themes

from ..services.appwrite import database_id, dbs, rooms_collection_id
from ..utils.constants import console, error_style, spinner, success_style
from ..utils.room import check_room_id, get_input, get_room
from ..utils.user import get_current_user

room_app = typer.Typer()


@room_app.command()
def create():
    """Create a new chat room for your project discussions"""
    current_user = get_current_user()
    name = typer.prompt("Enter the name of the room")
    description = typer.prompt("Enter the description of the room")
    room_id = typer.prompt("Enter a unique room id")
    check_room_id(room_id)

    data = {
        "name": name,
        "description": description,
        "room_id": room_id,
        "admin": current_user["name"],
        "admin_email": current_user["email"],
        "members": [current_user["email"]],
        "messages": [
            json.dumps(
                {
                    "id": current_user["email"],
                    "username": current_user["name"],
                    "message": "Welcome to the room!",
                }
            )
        ],
    }
    spinner("Creating room...", 3)
    list_of_docs = dbs.list_documents(
        database_id,
        rooms_collection_id,
        [Query.equal("name", name), Query.equal("admin_email", data["admin_email"])],
    )
    if list_of_docs["total"] == 0:
        try:
            dbs.create_document(database_id, rooms_collection_id, ID.unique(), data)
            console.print(f"🦄 Created room {data['name']} successfully!", style=success_style)
        except AppwriteException as e:
            console.print(f"🚫 Error creating room! Try again. '{e.message}' ", style=error_style)
    else:
        console.print(f"🚫 Room with name {data['name']} already exists!", style=error_style)


@room_app.command()
def list_all():
    """List all the chat rooms created by you"""
    current_user = get_current_user()
    spinner("Fetching rooms...", 3)
    list_of_docs = dbs.list_documents(
        database_id, rooms_collection_id, [Query.equal("admin_email", current_user["email"])]
    )
    if list_of_docs["total"] == 0:
        console.print("🚫 You have not created any rooms yet!", style=error_style)
    else:
        console.print("🦄 Your rooms:", style=success_style)
        for doc in list_of_docs["documents"]:
            console.print(f"👉 {doc['name']}", style=success_style)


@room_app.command()
def info():
    """Gives info about a chat room in a table format"""
    room_name, room_id = get_input()
    spinner("Fetching info...", 3)
    list_of_docs = get_room(room_id, room_name)
    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} and id {room_id}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        ptable = ColorTable(
            ["Name", "Admin", "Member count", "Members list", "Message count"], theme=Themes.OCEAN
        )
        ptable.add_row(
            [room["name"], room["admin"], len(room["members"]), room["members"], len(room["messages"])]
        )
        console.print(f"🦄 Info about room {room_name} with id {room_id}:", style=success_style)
        print(ptable)


@room_app.command()
def join():
    """Join an existing chat room"""
    current_user = get_current_user()
    room_name, room_id = get_input()
    spinner("Joining room...", 3)
    list_of_docs = get_room(room_id, room_name)

    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} and id {room_id}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        if current_user["email"] in room["members"]:
            console.print(
                f"🚫 You are already a member of {room_name} with id {room_id}!",
                style=error_style,
            )
        else:
            room["members"].append(current_user["email"])
            updated_members = {"members": room["members"]}
            try:
                dbs.update_document(database_id, rooms_collection_id, room["$id"], updated_members)
                console.print(
                    f"🦄 Joined room {room_name} with id {room_id}" " successfully!",
                    style=success_style,
                )
            except AppwriteException as e:
                console.print(f"🚫 Error joining room! Try again. '{e.message}' ", style=error_style)


@room_app.command()
def leave():
    """Leave a chat room"""
    current_user = get_current_user()
    room_name, room_id = get_input()
    spinner("Leaving room...", 3)
    list_of_docs = get_room(room_id, room_name)

    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} and id {room_id}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        if current_user["email"] not in room["members"]:
            console.print(
                f"🚫 You are not a member of {room_name} with id {room_id}!",
                style=error_style,
            )
        else:
            room["members"].remove(current_user["email"])
            updated_members = {"members": room["members"]}
            try:
                dbs.update_document(database_id, rooms_collection_id, room["$id"], updated_members)
                console.print(
                    f"🦄 Left room {room_name} with id {room_id}" " successfully!",
                    style=success_style,
                )
            except AppwriteException as e:
                console.print(f"🚫 Error leaving room! Try again. '{e.message}' ", style=error_style)


@room_app.command()
def delete():
    """Delete a chat room"""
    current_user = get_current_user()
    room_name = typer.prompt("Enter the name of the room you want to delete")
    spinner("Deleting room...", 3)
    list_of_docs = dbs.list_documents(
        database_id,
        rooms_collection_id,
        [Query.equal("name", room_name), Query.equal("admin_email", current_user["email"])],
    )

    if list_of_docs["total"] == 0:
        console.print(f"🚫 Room with name {room_name} does not exist!", style=error_style)
    else:
        room = list_of_docs["documents"][0]
        try:
            dbs.delete_document(database_id, rooms_collection_id, room["$id"])
            console.print(f"🦄 Deleted room {room_name} successfully!", style=success_style)
        except AppwriteException as e:
            console.print(f"🚫 Error deleting room! Try again. '{e.message}' ", style=error_style)
