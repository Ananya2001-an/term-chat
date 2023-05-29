from appwrite.query import Query
from ..services.appwrite import dbs, database_id, rooms_collection_id
from appwrite.exception import AppwriteException


def get_room(admin_email: str, name: str = None) -> dict | None:
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
