# MAIN FILE
from funcs import (
    deco,
    draw,
    list_input,
    log,
    setup_database,
    open_pass,
    list_pass,
    create_pass,
    modify_pass,
    delete_pass,
    generate_strong_password,
)
import sys

# from consts import OPTIONS_MAIN_MENU, FILE_PASS
from getpass import getpass
import pickle
import os
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

    # MENU FUNCTIONS
    OPTIONS_MAIN_MENU = {
        "List Items": {"func": list_pass, "args": [connection]},
        "Open Item": {"func": open_pass, "args": [connection]},
        "Create Item": {"func": create_pass, "args": [connection]},
        "Modify Items": {"func": modify_pass, "args": [connection]},
        "Delete Items": {"func": delete_pass, "args": [connection]},
        "Generate Strong Password": {"func": generate_strong_password, "args": []},
        "Exit": {"func": sys.exit, "args": [0]},
}

    # Menu
    while True:
        choice = draw("Menu", list_input, OPTIONS_MAIN_MENU)
        draw(f"Menu > {choice}", OPTIONS_MAIN_MENU[choice]["func"], *OPTIONS_MAIN_MENU[choice]["args"])
        input("Press enter to continue...")
