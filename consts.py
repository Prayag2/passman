# CONSTANTS AND VARIABLES
from sys import platform
import os
import string

DASHES_NO = 40

ALPHA_LOW = string.ascii_lowercase
ALPHA_UP = string.ascii_uppercase
DIGITS = string.digits
PUNCT = "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
ALL = ALPHA_LOW + ALPHA_UP + DIGITS + PUNCT + " "

HELP_TEXT = """*Passman, An Incredibly Simple Password Manager*\n
Passman is a simple password manager that allows you to store your passwords in a secure manner.
All of your passwords are stored in a MySQL database, and are encrypted so they are super secure.

#1 WHY PASSMAN?
***************
It lets you choose a unique and strong password for every website you visit.
This will make your life easier as you won't have to remember your passwords anymore.
This will prevent others from stealing your passwords.

#2 HOW TO USE PASSMAN?
**********************
Passman is a menu driven program that allows you to create, modify, and delete passwords.
You will be greeted with a nice menu, and you will be able to choose from the options provided.
There are seven options:
- List Credentials: Lists all of the credentials you have stored.
- Open Credential: Allows you to show details of a specific credential.
- Create Credential: Allows you to create a new credential.
- Modify Credentials: Allows you to modify an existing credential.
- Delete Credentials: Allows you to delete an existing credential.
- Generate Strong Password: Generates a strong password.
- Help: Displays this menu.
- Exit: Exits the program.

Each credential has a name and you can store your username & password with the URL of the website.
If you just want to create a strong password without saving it, you can use the "Generate Strong Password" option.

#3 AUTHOR
*********
This program was created by Prayag Jain from Manav Rachna International School.

#4 BUGS
*******
If you find any bugs, please report them here: https://github.com/prayag2/passman/issues

#5 LICENSE
**********
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. Read more here: https://www.gnu.org/licenses/gpl-3.0.en.html
"""
