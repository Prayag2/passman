# FUNCS
import sys
import random
import os
import mysql.connector as sql
from getpass import getpass
from consts import DASHES_NO, PUNCT, DIGITS, ALPHA_UP, ALPHA_LOW, ALL


def cinput(text, *args, sep=" ", end=""):
    """
    Custom input function.
    Args:
        text (str): The text to be displayed.
        *args (str): The arguments to be displayed.
        sep (str): The separator between the arguments.
        end (str): The end of the input.
    Returns:
        str: The input.
    """
    if args:
        text += sep.join(args)
    return input(text.title() + "\n❯ " + end)


def clear():
    """
    Clears the screen.
    Args:
        None
    Returns:
        None
    """
    os.system("cls" if os.name == "nt" else "clear")


def log(text, log_type="info"):
    """
    Logs text to the console.
    Args:
        text (str): The text to be logged.
        log_type (str): The type of log.
    Returns:
        None
    """
    if log_type == "info":
        print("[INFO] " + text)
    elif log_type == "error":
        print("[ERROR] " + text)
        sys.exit(-1)
    elif log_type == "warning":
        print("[WARNING] " + text)
    else:
        print("[UNKNOWN] " + text)


def dash(n=DASHES_NO):
    """
    Prints a line of dashes.
    Args:
        n (int): The number of dashes.
    Returns:
        None
    """
    print("=" * DASHES_NO)


def deco(text, expression="tb"):
    """
    Prints a line of dashes below or above the text.
    Args:
        text (str): The text to be displayed.
        expression (str): The expression to be used.
    Returns:
        None
    """
    # Centering text
    margin = (DASHES_NO - len(text)) // 2
    spaces = " " * margin if margin <= DASHES_NO else ""

    if "t" in expression:
        dash()
    print(spaces + text + spaces)
    if "b" in expression:
        dash()


def draw(heading, func, *args):
    """
    Draws a menu.
    Args:
        heading (str): The heading of the menu.
        func (function): The function to be called.
        *args (str): The arguments to be passed to the function.
    Returns:
        None
    """
    # Printing the heading and running the function
    deco(heading)
    val = func(*args)
    return val


def list_input(options, text=""):
    """
    Lists options and returns the user's choice.
    Args:
        options (dict): The options to be displayed.
        text (str): The text to be displayed.
    Returns:
        str: The user's choice.
    """

    for i, option in enumerate(options):
        print(f"{i+1}. {option.title()}")
    return list(options.keys())[int(cinput(text)) - 1]


def generate_random_string(length, digits=True, upper=True, punct=True):
    """
    Generates a random string.
    Args:
        length (int): The length of the string.
        digits (bool): Whether to include digits.
        upper (bool): Whether to include uppercase characters.
        punct (bool): Whether to include punctuation.
    Returns:
        str: The generated string."""

    passwd = ""
    characters = [x for x in ALPHA_LOW]
    if digits:
        characters.extend(DIGITS)
    if upper:
        characters.extend(ALPHA_UP)
    if punct:
        characters.extend(PUNCT)

    for i in range(length):
        passwd += random.choice(characters)

    return passwd


def generate_strong_password():
    """
    Generates a strong password.
    Args:
        None
    Returns:
        str: The generated password.
    """

    length = cinput("Enter length")
    punct = cinput("Would you like to include special characters? (Y/n)").lower()
    upper = cinput("Would you like to include uppercase characters? (Y/n)").lower()
    digits = cinput("Would you like to include digits? (Y/n)").lower()

    if punct == "n":
        punct = False
    if upper == "n":
        upper = False
    if digits == "n":
        digits = False
    if not length:
        length = 15

    password = generate_random_string(int(length), digits, upper, punct)

    # print the password
    deco(f"Here's your password: {password}")

    # Return the password
    return password


def encrypt_pass(password):
    """
    Encrypts the password.
    Args:
        password (str): The password to be encrypted.
    Returns:
        str: The encrypted password.
    """

    # Generate a random key
    key = [x for x in ALL]
    random.shuffle(key)
    key = "".join(key)

    # Encrypted password as an empty string
    encrypted_pass = ""

    # Encrypting the password by replacing the original character with the encrypted character
    for char in password:
        index = ALL.index(char)
        encrypted_pass += key[index]

    # Returning the encrypted password and the key
    return encrypted_pass, key


def decrypt_pass(encrypted_pass, key):
    """
    Encrypts the password.
    Args:
        password (str): The password to be encrypted.
    Returns:
        str: The encrypted password.
    """
    # Password as an empty string
    passwd = ""

    # Decrypting the password by replacing the encrypted character with the original character
    for i in range(len(encrypted_pass)):
        index = key.index(encrypted_pass[i])
        passwd += ALL[index]

    # Returning the decrypted password
    return passwd


def exec_query(connection, query):
    """
    Fetches all data from the database.
    """
    # Get the details
    cursor = connection.cursor()
    cursor.execute("USE passman")
    cursor.execute(query)
    try:
        result = cursor.fetchall()
    except sql.errors.InterfaceError:
        result = None
    connection.commit()
    cursor.close()
    return result


def setup_database(connection):
    """
    Sets up the database.
    Args:
        connection (sql.connector): The connection to the database.
    Returns:
        None
    """

    # Create a database in mysql named "passman"
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS passman")
    connection.commit()
    cursor.close()

    # Create a table in the database named "auth"
    # This table will store the username and password for
    # The `new_user` column stores a boolean to tell whether it is a new user or not
    exec_query(
        connection,
        "CREATE TABLE IF NOT EXISTS auth (username VARCHAR(255), password VARCHAR(1000), auth_key VARCHAR(1000), new_user TINYINT(1))",
    )
    exec_query(connection, "INSERT INTO auth (new_user) VALUES (1)")

    # Create a table in mysql named "passman"
    exec_query(
        connection,
        "CREATE TABLE IF NOT EXISTS passman\
        (id INT AUTO_INCREMENT PRIMARY KEY, \
        name VARCHAR(255), username VARCHAR(255), \
        password VARCHAR(2000), \
        url VARCHAR(255))",
    )

    # Create a table in mysql named "pass_keys"
    exec_query(
        connection,
        "CREATE TABLE IF NOT EXISTS pass_keys\
        (id INT AUTO_INCREMENT PRIMARY KEY, \
        pass_key VARCHAR(2000))",
    )


def reset_id(connection, table):
    """
    Resets the order of IDs of a table.
    Args:
        connection (sql.connector): The connection to the database.
        table (str): The table to be reset.
    Returns:
        None
    """

    # Get the id of the last row
    data = exec_query(connection, f"SELECT * FROM {table}")
    new_data = []

    # Removing "id" from every column
    for row in data:
        new_row = row[1::]
        new_data.append(new_row)

    # Get column names
    desc = exec_query(connection, f"DESC {table}")
    columns = [row[0] for row in desc][1::]
    columns = ", ".join(columns)

    # Deleting data from the table
    exec_query(connection, f"DROP TABLE {table}")

    # Creating all tables again
    setup_database(connection)

    # Adding new data to the table
    for row in new_data:
        if len(row) == 1:
            row = str(row)[:-2] + ")"
        exec_query(connection, f"INSERT INTO {table}({columns}) VALUES {row}")


def list_pass(connection):
    """
    Displays all records in the database.
    Args:
        connection (sql.connector): The connection to the database.
    Returns:
        None
    """
    result = exec_query(connection, "SELECT * FROM passman")

    if not result:
        log("No records found", log_type="info")
        return

    for row in result:
        print(f"{row[0]}. {row[1]}")


def open_pass(connection):
    """
    Lists all passwords.
    """

    # Get the details
    try:
        name = cinput("Enter Credential Name/ID").lower()
        if name.isdigit():
            result = exec_query(connection, f"SELECT * FROM passman WHERE id={name}")
            key = exec_query(
                connection, f"SELECT pass_key FROM pass_keys WHERE id={name}"
            )[0][0]
        else:
            result = exec_query(
                connection, f"SELECT * FROM passman WHERE name='{name}'"
            )
            key = exec_query(
                connection,
                f"SELECT pass_key FROM pass_keys WHERE id=(SELECT id FROM passman WHERE name='{name}')",
            )[0][0]
    except:
        log("No such Credential", log_type="warning")
        return

    for row in result:
        print(f"Name: {row[1]}")
        print(f"Username: {row[2]}")
        print(f"Password: {decrypt_pass(row[3], key)}")
        print(f"Website URL: {row[4]}")


def create_pass(connection):
    """
    Creates a password.
    """
    # Get the details
    name = cinput("Enter Credential Name")
    username = cinput("Enter Username/Email")
    password = cinput("New Password ('g' to generate a strong password)")

    # If the input is 'g', generate a strong password
    if password.lower() == "g":
        deco("Generate Strong Password", "tb")
        password = generate_strong_password()

    # Encrypting the password
    password, key = encrypt_pass(password)
    url = cinput("Enter Website URL")

    # insert data in database
    exec_query(
        connection,
        f"INSERT INTO passman (name, username, password, url) VALUES ('{name}', '{username}', '{password}', '{url}')",
    )
    exec_query(connection, f"INSERT INTO pass_keys(pass_key) VALUES ('{key}')")

    deco("Credential created successfully!", "t")


def modify_pass(connection):
    """
    Modifies password.
    """
    # Get the details
    name = cinput("Search Credential Name/ID").lower()
    if not exec_query(
        connection, f"SELECT * FROM passman WHERE id='{name}'"
    ) and not exec_query(connection, f"SELECT * FROM passman WHERE name='{name}'"):
        log("No such Credential", log_type="warning")
        return

    dash()
    new_name = cinput("Enter New Credential Name")
    username = cinput("New Username/Email")
    password = cinput("New Password ('g' to generate a strong password)")

    # If the input is 'g', generate a strong password
    if password.lower() == "g":
        password = generate_strong_password()

    # Encrypting the password
    password, key = encrypt_pass(password)
    url = cinput("New Website URL")

    # update data in database
    if name.isdigit():
        exec_query(
            connection,
            f"UPDATE passman SET name='{new_name}', username='{username}', password='{password}', url='{url}' WHERE id={name}",
        )
        exec_query(
            connection, f"UPDATE pass_keys SET pass_key='{key}' WHERE id={new_name}"
        )
    else:
        exec_query(
            connection,
            f"UPDATE passman SET name='{new_name}', username='{username}', password='{password}', url='{url}' WHERE name='{name}'",
        )
        exec_query(
            connection,
            f"UPDATE pass_keys SET pass_key='{key}' WHERE id=(SELECT id FROM passman WHERE name='{new_name}')",
        )

    # Print success message
    deco("Credential modified successfully!", "t")


def delete_pass(connection):
    """
    Deletes a password.
    Args:
        connection (sql.connector): The connection to the database.
    Returns:
        None
    """
    # Get the details
    name = cinput("Enter Credential Name/ID").lower()
    if not exec_query(
        connection, f"SELECT * FROM passman WHERE id='{name}'"
    ) and not exec_query(connection, f"SELECT * FROM passman WHERE name='{name}'"):
        log("No such Credential", log_type="warning")
        return

    # Confirm delete
    confirm = cinput("Do you really want to delete this Credential? (y/n)").lower()
    if not confirm == "y":
        return

    # delete data from database
    if name.isdigit():
        exec_query(connection, f"DELETE FROM passman WHERE id={name}")
        exec_query(connection, f"DELETE FROM pass_keys WHERE id={name}")
    else:
        exec_query(
            connection,
            f"DELETE FROM pass_keys WHERE id=(SELECT id FROM passman WHERE name='{name}')",
        )
        exec_query(connection, f"DELETE FROM passman WHERE name='{name}'")

    # reset order of IDs
    reset_id(connection, "passman")
    reset_id(connection, "pass_keys")

    # Print success message
    deco("Password deleted successfully!", "t")
