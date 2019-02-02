<h1>**MTG Tracker**</h1>
An app for your Magic: The Gathering collection.
<hr>
<h2>**Installation**</h2>
<hr>
<h3>Prerequisites</h3>
- [Install Python3](https://www.python.org/downloads/ "Python.org Downloads") on your system.

- [Install PostgreSQL](https://www.postgresql.org/download/ "PostgreSQL Downloads") on your system.

- Clone this repository, then `cd` into the `mtgtracker` directory

<h3>Set up a virtual environment</h3>
- Once inside `mtgtracker/`, create a virtual environment with `python3 -m venv env`

- Activate your virtual environment with `source env/bin/activate`

- Run `pip3 install -r ./requirements/development.txt` to install all dependencies necessary for local development.
Refer to `requirements/production.txt` for production-specific dependencies.

<h3>Set up environment variables</h3>
- Generate a `SECRET_KEY` by entering this code into the command line. Save the `SECRET_KEY` (a string of random letters/numbers/symbols that will print to the command line), you'll need it in a second:

  `python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

- Open `env/bin/activate` and insert the following content on line 35/36:
  ```
  unset DJANGO_SETTINGS_MODULE
  unset SECRET_KEY
  unset PGDB_NAME
  unset PGDB_USER
  unset PGDB_PASS
  ```

  Lines 34-41 should now look like this:

  ```
  34    fi
  35
  36    unset DJANGO_SETTINGS_MODULE
  37    unset SECRET_KEY
  38    unset PGDB_NAME
  39    unset PGDB_USER
  40    unset PGDB_PASS
  41  }
  ```

- Insert the following content at the end of the file, starting on line 84, replacing the necessary lines with your specific information:

  ```
  export DJANGO_SETTINGS_MODULE="tome.settings.development"
  export SECRET_KEY="replace_with_the_generated_secret_key_you_just_made"
  export PGDB_NAME="tome"
  export PGDB_USER="replace_this_with_the_username_you_set_in_psql"
  export PGDB_PASS="replace_this_with_the_password_you_set_in_psql"
  ```

- Close the file. Since we have altered the virtual environment's activation script, we must leave and re-enter the virtual environment for our changes to take effect.

- Leave the virtual environment with `deactivate`

- Re-enter the virtual environment with `source env/bin/activate`

<h3>Create a new user and database in Postgres</h3>
- Open Postgres from the terminal by typing: `psql`

- Create a new Postgres user with a username and password of your choosing, using single quotes around your password.

  `CREATE USER your_user_name WITH PASSWORD 'your_password';`

- Create a new database and make your new user the owner:

  `CREATE DATABASE tome WITH OWNER your_user_name;`

- Exit `psql` by typing `\q`

<h3>Set up the database schema and load in card data</h3>
- Make migrations with `python3 manage.py makemigrations`

- Migrate the schema with `python manage.py migrate`

- Enter the following on the command line to populate the database with all card data from the [MTG SDK](https://github.com/MagicTheGathering/mtg-sdk-python "MTG SDK Github"). This might take several minutes, so go play a quick game of Magic.

  `python manage.py update_db_card_database`

- When `update_db_card_database` has finished, you will see an `Update successful` message on the command line indicating a successful transfer. If you see an error message instead, please submit a new issue to us!

<h3>Create a Django superuser and run the server</h3>
- Enter the following into the command line to create a superuser for the Django project. Follow the prompts that appear:

  `python manage.py createsuperuser`

- Start up the server with `python manage.py runserver`

- Visit `http://127.0.0.1:8000/` to use the app!
<hr>
