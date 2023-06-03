## How to contribute to term-chat 💬
Thanks for deciding to contribute to the term-chat project 💙 You have to follow the below steps for proper contribution flow.

- Kindly ask for assigning to an issue before raising a PR.
- If your issue is not present in the current issues list then you can create one.
- Only if the issue gets approved you should start working on it.
- Now follow the below **Development** section to start developing on your local machine.
- Later raise a PR to this repository's main branch for code review.
- If the PR gets approved, it will be merged!

## 💻 Development:

First of all, make sure you have the following requirements:
- Python 3.8 or higher
- [Poetry](https://python-poetry.org/)
- [Appwrite Cloud](https://cloud.appwrite.io/)

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

3. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

4. Create dotenv file and add necessary environment variables for the database connection:

   ```bash
   cp .env.example .env
   ```

5. Run the tests to make sure everything is working as expected (make sure to define attributes and indices for the Appwrite collection):

   ```bash
    poetry run pytest -v
    ```

6. Run the application:

   ```bash
   python -m term_chat --help
   ```
   
Yay! Now you can experiment with the code as such as you want :)
