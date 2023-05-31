import os

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from dotenv import load_dotenv

load_dotenv()

client = Client()

(
    client.set_endpoint("https://cloud.appwrite.io/v1")
    .set_project(os.getenv("APPWRITE_PROJECT_ID"))
    .set_key(os.getenv("APPWRITE_SECRET_API_KEY"))
)

users = Users(client)
dbs = Databases(client)

database_id = os.getenv("APPWRITE_DATABASE_ID")  # term-chat db
rooms_collection_id = os.getenv("APPWRITE_COLLECTION_ID")  # project-rooms collection
