import json
# to store the nested dictionary use json file, so its load the dictionary in the memory evertime


def menu():
    print("\n========== CLI Password Manager =========\n")

    print("1. Add Account")
    print("2. check Password")
    print("3. Display Websites")
    print("4. update Password")
    print("5. Delete Account")
    print("6. View all Accounts")
    print("7. Exit\n")

    return input("Enter a choice: ")


def choose_one(choice, total_accounts):
    if choice == "1":
        print("\n--->>> Add Account")
        total_accounts = add_account(total_accounts)
        print("\n Account added successfully")
    elif choice == "2":
        print(" --->>> check Password")
        check_password(total_accounts)
    elif choice == "3":
        print("--->>> List of Websites")
        display_websites(total_accounts)
    elif choice == "4":
        print("update")
        update_password(total_accounts)
    elif choice == "5":
        print("--->>> Delete Account")
        delete_account(total_accounts)
    elif choice == "6":
        view_accounts(total_accounts)
    elif choice == "7":
        print("Thank you")
        return False
    else:
        print("\n           invalid choice!!")

    return True


def update_password(accounts):

    if_update = True

    print("\n Websites: ")
    display_websites(accounts)
    website = get_website_name(accounts)
    email_lists = list_of_emails_in_a_website(website, accounts)
    updated_account = choose_email_to_check_or_update_its_password(
        accounts, website, email_lists, len(email_lists), if_update
    )
    save_accounts(updated_account)


def delete_account(accounts):
    display_websites_emails(accounts)

    print("\n 1 -> Delete Account \n 2 -> Delete website \n 0 -> Back")

    while True:
        try:
            chosen_no = int(input("    choose 1, 2 or 0: "))
        except ValueError:
            print("invalid input")
            continue
        if chosen_no not in {1, 2, 0}:
            print("invalid choice")
            continue
        if chosen_no == 0:
            return
        break

    while True:
        website_to_be_deleted = input("Enter website: ")

        for website in accounts:
            if website_to_be_deleted == website:
                print("inside ")
                if chosen_no == 1:
                    list_emails = list(accounts[website].keys())
                    print(website + " emails: ", list_emails)
                    if len(list_emails) == 1:
                        while True:
                            valid_input = input(
                                "do you want to delete " + list_emails[0] + " [y/n]: "
                            )
                            if valid_input == "y" or valid_input == "Y":
                                del accounts[website_to_be_deleted]
                                print(" deleted successfully")
                                save_accounts(accounts)
                                return
                            elif valid_input == "n" or valid_input == "N":
                                return
                            else:
                                print("invalid input")
                    else:
                        while True:
                            email_to_be_deleted = make_valid_email()
                            for email in list_emails:
                                if email == email_to_be_deleted:
                                    del accounts[website_to_be_deleted][
                                        email_to_be_deleted
                                    ]
                                    print("  deleted successfully")
                                    save_accounts(accounts)
                                    return
                                continue
                            print(
                                "\n "
                                + email_to_be_deleted
                                + " is not present in "
                                + website_to_be_deleted
                            )
                            print("\n emails listed: ", list_emails)

                else:
                    del accounts[website]
                    print(website + " deleted successfully")
                    save_accounts(accounts)
                    return
            continue
        print(" website not found ")


def view_accounts(total_accounts):
    if total_accounts == {}:
        print("No account found\n   press 1 to add Account")
        return
    display_websites_emails(total_accounts)


def display_websites_emails(accounts):
    for website in accounts:
        print("\n[-] " + website + ":")
        list_of_emails_in_a_website(website, accounts)


def display_websites(accounts):
    for website in accounts:
        print("-->> " + website)


def add_account(accounts):

    website_name = make_valid_website()

    # if we need to add emails to the same website
    if website_name in accounts:
        accounts = add_email_to_existing_website(accounts, website_name)

    # if the website is new, just add a new dictionary
    else:
        email = make_valid_email()
        password = make_valid_password()
        accounts[website_name] = {email: {"Password": password}}
    return save_accounts(accounts)


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


def list_of_emails_in_a_website(website, accounts):
    email_lists = list(accounts[website].keys())

    print("\n---> emails linked with " + website + " : ")
    i = 1
    for email in email_lists:
        print(" " + str(i) + ". " + email)
        i = i + 1
    return email_lists


def get_website_name(accounts):
    while True:
        website_name = input("enter website name: ")
        if website_name in accounts:
            return website_name
        print(website_name + " not found")
        continue


def check_password(available_accounts):
    if_update = False
    if available_accounts == {}:
        print("    No website present")
        return
    display_websites(available_accounts)

    website_name = get_website_name(available_accounts)
    email_lists = list_of_emails_in_a_website(website_name, available_accounts)
    length_email_list = len(email_lists)

    choose_email_to_check_or_update_its_password(
        available_accounts,
        website_name,
        email_lists,
        length_email_list,
        if_update,
    )


def choose_email_to_check_or_update_its_password(
    available_accounts, website_name, email_lists, length_email_list, if_update
):

    if length_email_list == 1:
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


def save_accounts(accounts):
    with open("stored_accounts.json", "w") as file:
        return json.dump(accounts, file, indent=4)


def load_accounts():

    try:
        with open("stored_accounts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # empty dict, if no data present
    except PermissionError:
        print("you do not have permission to access the stored_accounts.json file")


def clear_screen():
    # \033[H moves cursor to top-left, \033[2J clears the screen
    print("\033[H\033[2J", end="")


def main():

    load_stored_accounts = load_accounts()

    check_if = True

    while check_if:
        choice = menu()
        check_if = choose_one(choice, load_stored_accounts)
        if check_if:
            input("\n     press enter to go back to menu : ")
            clear_screen()
        else:
            break


main()
