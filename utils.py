import secrets

from cryptography.fernet import Fernet

from crypto import load_key, make_encrypted_file


# def search_suggestion(accounts, website):


def save_accounts(accounts):
    key = load_key()
    cipher_suite = Fernet(key)

    make_encrypted_file(cipher_suite, accounts)


def choose_email_to_check_or_update_its_password(
    available_accounts, website_name, email_lists, length_email_list, if_update
):

    if length_email_list == 1:
        if if_update:
            print(
                "current Password: "
                + available_accounts[website_name][email_lists[0]]["Password"]
            )

            print("Enter new Password: ")
            new_password = make_valid_password()

            print("Password updated to : " + new_password)
            available_accounts[website_name][email_lists[0]]["Password"] = new_password
            return available_accounts
        print(
            "Password: " + available_accounts[website_name][email_lists[0]]["Password"]
        )
        return

    print("\nChoose any email to check its Passwords, enter the above no(1 or 2 ...)")
    print("To return to the menu, press 0: ")
    select = 0
    while True:
        try:
            select = int(input("Enter here: "))

        except ValueError:
            print(
                "....Not a digit, select a digit less than "
                + str(length_email_list + 1)
            )

        if select == 0:
            return
        elif select <= length_email_list and select > 0:
            if if_update:
                print(
                    "current Password: "
                    + available_accounts[website_name][email_lists[select - 1]][
                        "Password"
                    ]
                )

                print("Enter new Password: ")
                new_password = make_valid_password()

                print("Password updated to : " + new_password)
                available_accounts[website_name][email_lists[select - 1]][
                    "Password"
                ] = new_password
                return available_accounts

            print(
                "Password: "
                + available_accounts[website_name][email_lists[select - 1]]["Password"]
            )

            print(
                "press '0' to go back, else enter valid no to check other Passwords: "
            )
        else:
            print("please select a digit less than " + str(length_email_list + 1))


def make_valid_website():
    # first character cannot be -  .  space or any special character
    # only letters and numbers allowed
    while True:
        website = input("Website: ")

        if len(website) == 0 or not website[0].isalnum():
            print(
                "...invalid website name!!\n First character must belong to either the alphabet (a-z, A-Z) or digits (0-9) \n"
            )
        else:
            return website


def make_valid_email():
    while True:
        email = input("\nemail: ")
        if len(email) > 10:
            length_email = len(email)
            position_of_email_domain = length_email - 10  # @gmail.com --> 10 letters
            email_domain = ""

            for i in range(position_of_email_domain, length_email):
                email_domain = email_domain + email[i]

            if email_domain == "@gmail.com":
                return email
        print("......invalid email!!\n please try like: username@gmail.com")


def add_email_to_existing_website(accounts, website):
    while True:
        # email = input('email: ')
        email = make_valid_email()
        email_lists = list(accounts[website].keys())
        if email in email_lists:
            print(email + " already exists\n  ...Please enter different_email")
        else:
            password = make_valid_password()
            accounts[website][email] = {"Password": password}
            break
    return accounts


def make_valid_password():

    while True:
        user_input = input("Generate password? (y/n) ")

        if user_input == "y" or user_input == "Y":
            return generate_password()
        elif user_input == "n" or user_input == "N":
            return manual_password()
        else:
            print("\n  invalid selection!!")


def manual_password():

    # Password should not be less than 6 characters
    # every Password must be unique
    password = ""

    while True:
        password = input("\n  Password atleast 6 char  ----> ")
        if len(password) < 6:
            print(" .....password must contain atleast 6 characters ")

        else:
            no_error = True
            for char in password:
                if char == " ":
                    print("invalid password....password cannot contain blank space...")
                    no_error = False
                    break
            if no_error:
                return password


def get_website_name(accounts):
    while True:
        website_name = input("enter website name: ")
        if website_name in accounts:
            return website_name
        print(website_name + " not found")
        continue


def list_of_emails_in_a_website(website, accounts):
    email_lists = list(accounts[website].keys())

    if len(email_lists) == 1:
        print("email: ", email_lists[0])
        return email_lists
    print("\n---> emails linked with " + website + " : ")
    i = 1
    for email in email_lists:
        print(" " + str(i) + ". " + email)
        i = i + 1
    return email_lists


def display_websites_emails(accounts):
    for website in accounts:
        print("\n[-] " + website + ":")
        list_of_emails_in_a_website(website, accounts)


def accounts_exists(accounts):
    if accounts == {}:
        return False
    return True


def generate_password():
    # generate atleast 6 char password
    # it can contain letters(upper lower), digits, symbols
    # generate each char randomly
    # add all and return the Password

    # random() is predictable so for more security we used secrets()

    omit_char = {
        ord('"'),
        ord(","),
        ord("`"),
        ("("),
        ord(")"),
        ord("<"),
        ord(">"),
        ord("\\"),
        ord("."),
        ord("'"),
        ord("["),
        ord("]"),
    }
    while True:
        ask_password_length = 0
        try:
            ask_password_length = int(input("Length ? (Default: 16) "))
        except ValueError:
            if (
                ask_password_length == 0
            ):  # if user press enter --> generate 16 digit password
                ask_password_length = 16
            else:
                print("\ninvalid input \n")
                continue

        if ask_password_length >= 8:
            ascii_characters = ""
            for ascii_decimal_value in range(ord("!"), ord("~")):
                if ascii_decimal_value in omit_char:
                    continue

                ascii_characters = ascii_characters + chr(ascii_decimal_value)
            generate_password = ""
            for i in range(ask_password_length):
                generate_password = generate_password + secrets.choice(ascii_characters)
            return generate_password
        print("\n  atleast 8 character")
        continue
