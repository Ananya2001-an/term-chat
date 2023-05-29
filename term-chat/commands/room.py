import typer
import os
import pickle
import json
from ..utils.constants import error_style, success_style, console, spinner

from ..services.appwrite import dbs, database_id, rooms_collection_id
from appwrite.id import ID
from appwrite.exception import AppwriteException
from ..utils.user import get_current_user
from ..utils.room import get_room

room_app = typer.Typer()


@room_app.command()
def create():
    """Create a new chat room for your project discussions"""
    current_user = get_current_user()
    data = {
        "name": typer.prompt("Enter the name of the room"),
        "description": typer.prompt("Enter the description of the room"),
        "admin": current_user["name"],
        "admin_email": current_user["email"],
        "members": [current_user["email"]],
        "messages": [json.dumps({"id": current_user["email"], "message": "Welcome to the room!"})],
    }
    spinner("Creating room...", 3)
    list_of_docs = get_room(data["admin_email"], data["name"])
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
    list_of_docs = get_room(admin_email=current_user["email"])
    if list_of_docs["total"] == 0:
        console.print("🚫 You have not created any rooms yet!", style=error_style)
    else:
        console.print("🦄 Your rooms:", style=success_style)
        for doc in list_of_docs["documents"]:
            console.print(f"👉 {doc['name']}", style=success_style)


@room_app.command()
def list_members():
    """List the members of a chat room"""
    current_user = get_current_user()
    room_name = typer.prompt("Enter the name of the room you want to see members of")
    room_admin_email = typer.prompt("Enter the email of the admin of the room")
    spinner("Fetching members...", 3)
    list_of_docs = get_room(room_admin_email, room_name)
    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} under admin {room_admin_email}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        console.print(f"🦄 Members of {room_name} under admin {room_admin_email}:", style=success_style)
        for member in room["members"]:
            console.print(f"👉 {member}", style=success_style)


@room_app.command()
def join():
    """Join an existing chat room"""
    current_user = get_current_user()
    room_name = typer.prompt("Enter the name of the room you want to join")
    room_admin_email = typer.prompt("Enter the email of the admin of the room")
    spinner("Joining room...", 3)
    list_of_docs = get_room(room_admin_email, room_name)

    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} under admin {room_admin_email}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        if current_user["email"] in room["members"]:
            console.print(
                f"🚫 You are already a member of {room_name} under" " admin {room_admin_email}!",
                style=error_style,
            )
        else:
            room["members"].append(current_user["email"])
            updated_members = {"members": room["members"]}
            try:
                dbs.update_document(database_id, rooms_collection_id, room["$id"], updated_members)
                console.print(
                    f"🦄 Joined room {room_name} under admin {room_admin_email}" " successfully!",
                    style=success_style,
                )
            except AppwriteException as e:
                console.print(f"🚫 Error joining room! Try again. '{e.message}' ", style=error_style)


@room_app.command()
def leave():
    """Leave a chat room"""
    current_user = get_current_user()
    room_name = typer.prompt("Enter the name of the room you want to leave")
    room_admin_email = typer.prompt("Enter the email of the admin of the room")
    spinner("Leaving room...", 3)
    list_of_docs = get_room(room_admin_email, room_name)

    if list_of_docs["total"] == 0:
        console.print(
            f"🚫 Room with name {room_name} under admin {room_admin_email}" " does not exist!",
            style=error_style,
        )
    else:
        room = list_of_docs["documents"][0]
        if current_user["email"] not in room["members"]:
            console.print(
                f"🚫 You are not a member of {room_name} under" " admin {room_admin_email}!",
                style=error_style,
            )
        else:
            room["members"].remove(current_user["email"])
            updated_members = {"members": room["members"]}
            try:
                dbs.update_document(database_id, rooms_collection_id, room["$id"], updated_members)
                console.print(
                    f"🦄 Left room {room_name} under admin {room_admin_email}" " successfully!",
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
    list_of_docs = get_room(current_user["email"], room_name)

    if list_of_docs["total"] == 0:
        console.print(f"🚫 Room with name {room_name} does not exist!", style=error_style)
    else:
        room = list_of_docs["documents"][0]
        try:
            dbs.delete_document(database_id, rooms_collection_id, room["$id"])
            console.print(f"🦄 Deleted room {room_name} successfully!", style=success_style)
        except AppwriteException as e:
            console.print(f"🚫 Error deleting room! Try again. '{e.message}' ", style=error_style)
