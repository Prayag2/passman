# MAIN FILE
from funcs import (
    dash,
    deco,
    decrypt_pass,
    draw,
    encrypt_pass,
    list_input,
    log,
    setup_database,
    open_pass,
    list_pass,
    create_pass,
    modify_pass,
    delete_pass,
    generate_strong_password,
    clear,
    cinput,
    exec_query,
)
from consts import HELP_TEXT
import sys
from getpass import getpass
import mysql.connector as sql


if __name__ == "__main__":

    # Setting up the database
    sql_pass = getpass("Enter MySQL Password (hidden): ")
    try:
        # Connect to MySQL
        connection = sql.connect(host="localhost", user="root", passwd=sql_pass)

    except sql.ProgrammingError as e:
        # If the password is incorrect, then exit
        log("Access denied.", log_type="error")

    except sql.errors.InterfaceError:
        # If the connection fails, then exit
        log("Invalid host.", log_type="error")

    else:
        # If the connection is successful, then continue
        # Setup the database
        setup_database(connection)

    # User Authentication
    auth_data = exec_query(connection, "SELECT * FROM auth")[0]

    # If it's a new user, then create a new account
    if auth_data[3] == 1:
        deco("First Time Setup")
        user = cinput("Choose a username")

        # Confirming password
        while True:
            passwd = cinput("Choose a password")
            confirm = cinput("Confirm password")
            if passwd == confirm:
                break
            else:
                log("Passwords do not match.", log_type="warning")

        # Encrypting password
        epass, key = encrypt_pass(passwd)

        # Storing username and password
        exec_query(
            connection,
            f"UPDATE auth SET username='{user}', password='{epass}', auth_key='{key}', new_user=0",
        )

        # Success Message
        dash()
        log("Setup complete. Run passman again to continue.")
        sys.exit(0)

    # If it's an existing user, then authenticate
    else:
        deco("Login")

        # Getting username and password
        user = cinput("Enter usename")
        passwd = cinput("Enter password")

        # Decrypting real password
        dpass = decrypt_pass(auth_data[1], auth_data[2])

        # Checking if username and password match
        if user == auth_data[0] and passwd == dpass:
            log("Login successful.")
        else:
            dash()
            log("Incorrect username/password.", log_type="error")

    # MENU FUNCTIONS
    OPTIONS_MAIN_MENU = {
        "List Credentials": {"func": list_pass, "args": [connection]},
        "Open Credential": {"func": open_pass, "args": [connection]},
        "Create Credential": {"func": create_pass, "args": [connection]},
        "Modify Credentials": {"func": modify_pass, "args": [connection]},
        "Delete Credentials": {"func": delete_pass, "args": [connection]},
        "Generate Strong Password": {"func": generate_strong_password, "args": []},
        "Help": {"func": deco, "args": [HELP_TEXT, ""]},
        "Exit": {"func": sys.exit, "args": [0]},
    }

    # Menu
    try:
        while True:
            clear()

            # Displaying the menu
            choice = draw("Menu", list_input, OPTIONS_MAIN_MENU)
            clear()

            # Running the selected function
            draw(
                f"Menu > {choice}",
                OPTIONS_MAIN_MENU[choice]["func"],
                *OPTIONS_MAIN_MENU[choice]["args"],
            )
            dash()
            input("\nPress enter to continue...")

            # If CTRL+C or CTRL+D is pressed, then exit
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(0)
    except SystemExit:
        print("\nExited.")
    except Exception as e:
        # If there is an error, print it nicely and exit
        log(f"{e}".title(), log_type="error")
