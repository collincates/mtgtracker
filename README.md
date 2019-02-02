<h3>Prerequisites</h3>
- [Install Python3](https://www.python.org/downloads/ "Python.org Downloads") on your system.

- [Install PostgreSQL](https://www.postgresql.org/download/ "PostgreSQL Downloads") on your system.

- Clone this repository, then go into the directory with `cd tome`.

<h3>Set up a virtual environment</h3>
- Create a virtual environment with `python3 -m venv env`.

- Activate your virtual environment with `source env/bin/activate`

- Run `pip3 install -r ./requirements/development.txt` to install all dependencies necessary for local development. Refer to `requirements/production.txt` for production-specific dependencies.

<h3>Set up environment variables</h3>
- Generate a `SECRET_KEY` by entering this code into the command line. Save this `SECRET_KEY` for the next step:

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
  export SECRET_KEY="replace_with_a_generated_secret_key_using_the_instructions_below"
  export PGDB_NAME="tome"
  export PGDB_USER="replace_this_with_the_username_you_set_in_psql"
  export PGDB_PASS="replace_this_with_the_password_you_set_in_psql"
  ```

<h3>Create a new user and database in Postgres</h3>
- Open Postgres from the terminal by typing: `psql`.

- Create a new Postgres user with a username and password of your choosing, using single quotes around your password.

  `CREATE USER your_user_name WITH PASSWORD 'your_password';`

- Create a new database and make your new user the owner:

  `CREATE DATABASE tome WITH OWNER your_user_name;`

- Exit `psql` by typing `\q`.



Migrate & test!
