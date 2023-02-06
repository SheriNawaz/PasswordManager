import random
import string
import pickle
import os


def view_passwords(passwords):
    print(passwords)
    choice = input("Would you like to change or delete any entries? (C/D): ")
    if choice.lower() == "d":
        item = input("Write name of service: ")
        del passwords[item]
    elif choice.lower() == "c":
        item = input("Write name of service: ")
        password_or_name = input("Username (U) or password (P)? ")
        if password_or_name.lower() == "u":
            new_name = input("Enter Username: ")
            passwords[item] = (new_name, passwords[item][1])
        elif password_or_name.lower() == "p":
            new_password = input("Enter Password: ")
            passwords[item] = (passwords[item][0], new_password)


def add_password(passwords):
    title = input("Input name of service: ")
    username = input("Input username: ")
    password = input("Input password: ")
    passwords[title] = [username, password]


def generate_password():
    length = int(input("Input number of characters: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    print(''.join(random.choice(characters) for i in range(length)))


def save_passwords(passwords):
    with open("passwords.p", "wb") as f:
        pickle.dump(passwords, f)


def load_passwords():
    if os.path.getsize("passwords.p") == 0:
        return {}
    with open("passwords.p", "rb") as f:
        return pickle.load(f)


def main():
    passwords = load_passwords()
    while True:
        choice = input("View Passwords (V), Add Password (A), Generate Password (G), Quit (Q): ")
        if choice.lower() == "v":
            view_passwords(passwords)
        elif choice.lower() == "a":
            add_password(passwords)
        elif choice.lower() == "g":
            generate_password()
        elif choice.lower() == "q":
            break
        else:
            print("Invalid Choice")
    save_passwords(passwords)


main()
