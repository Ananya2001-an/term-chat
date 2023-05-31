# term-chat

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/license/gpl-3-0/) 
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Ananya2001-an/term-chat)](https://github.com/Ananya2001-an/term-chat/releases)
![GitHub repo size](https://img.shields.io/github/repo-size/Ananya2001-an/term-chat)

**term-chat** is a simple command-line chat 💬 application written in Python🐍. It allows users to communicate with each other through a terminal interface.

![term-chat-demo](https://github.com/Ananya2001-an/term-chat/assets/55504616/12d49bd5-742f-4bb6-9f4a-7a2565f24b41)

## Commands 🎮

It's a Typer application, so you can use the `--help` flag to get a list of all the available commands.
In development mode, you can run the application using `python -m term_chat`. 

- Auth commands 

    - `auth create-user <username> <email id>`: Register a new user
    - `auth login <email id>`: Login as an existing user (creates a pickle file in the current directory)
    - `auth logout`: Logout the current user
    - `auth whoami`: Display the current user
    - `auth delete-user`: Delete the current logged in user from the database

- Room commands
    
    - `room create`: Create a new chat room
    - `room join`: Join an existing chat room
    - `room leave`: Leave a room that you have joined
    - `room info`: Get information about a chat room
    - `room list-all`: List all the chat rooms made by you
    - `room delete`: Delete a chat room that you have created

- Chat commands
    
    - `chat start`: Send a message to a chat room

## Features 💫

- Real-time chat: Users can send and receive messages in real-time.
- Multiple chat rooms: Users can join different chat rooms and interact with other users in each room.
- Simple and intuitive interface: The chat interface is designed to be user-friendly and easy to navigate.

## Requirements ✅

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/)

## Development/Installation 👩‍💻

1. Clone the repository:

   ```bash
    git clone https://github.com/Ananya2001-an/term-chat.git

    cd term-chat
    ```

2. Activate the virtual environment(optional but recommended):

   ```bash
   python -m venv venv
   venv/Scripts/activate
   ```

3. Install the dependencies:

   ```bash
   poetry install
   ```

4. Create dotenv file and add necesary environment variables for the database connection:

   ```bash
   cp .env.example .env
   ```

5. Run the tests to make sure everything is working as expected:

   ```bash
    poetry run pytest tests
    ```

6. Run the application:

   ```bash
   python -m term_chat --help
   ```

