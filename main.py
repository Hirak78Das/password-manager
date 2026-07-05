from cryptography.fernet import Fernet
from crypto import (
    decrypt_to_dict,
    make_encrypted_file,
    load_key,
)
import utils as ut


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


def add_account(accounts):

    website_name = ut.make_valid_website()

    # if we need to add emails to the same website
    if website_name in accounts:
        accounts = ut.add_email_to_existing_website(accounts, website_name)

    # if the website is new, just add a new dictionary
    else:
        email = ut.make_valid_email()
        password = ut.make_valid_password()
        accounts[website_name] = {email: {"Password": password}}
    return ut.save_accounts(accounts)


def check_password(available_accounts):
    if_update = False
    if ut.accounts_exists(available_accounts):
        display_websites(available_accounts)

        website_name = ut.get_website_name(available_accounts)
        email_lists = ut.list_of_emails_in_a_website(website_name, available_accounts)
        length_email_list = len(email_lists)

        ut.choose_email_to_check_or_update_its_password(
            available_accounts,
            website_name,
            email_lists,
            length_email_list,
            if_update,
        )
    else:
        print("\nNo available_accounts")
        return


def display_websites(accounts):
    if ut.accounts_exists(accounts):
        for website in accounts:
            print("-->> " + website)
    else:
        return


def update_password(accounts):

    if_update = True

    if ut.accounts_exists(accounts):
        print("\n Websites: ")
        display_websites(accounts)
        website = ut.get_website_name(accounts)
        email_lists = ut.list_of_emails_in_a_website(website, accounts)
        updated_account = ut.choose_email_to_check_or_update_its_password(
            accounts, website, email_lists, len(email_lists), if_update
        )
        ut.save_accounts(updated_account)
    else:
        print("\nNo accounts present")
        return


def delete_account(accounts):
    if ut.accounts_exists(accounts):
        ut.display_websites_emails(accounts)

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
                    if chosen_no == 1:
                        list_emails = list(accounts[website].keys())
                        print(website + " emails: ", list_emails)
                        if len(list_emails) == 1:
                            while True:
                                valid_input = input(
                                    "do you want to delete "
                                    + list_emails[0]
                                    + " [y/n]: "
                                )
                                if valid_input == "y" or valid_input == "Y":
                                    del accounts[website_to_be_deleted]
                                    print(" deleted successfully")
                                    ut.save_accounts(accounts)
                                    return
                                elif valid_input == "n" or valid_input == "N":
                                    return
                                else:
                                    print("invalid input")
                        else:
                            while True:
                                email_to_be_deleted = ut.make_valid_email()
                                for email in list_emails:
                                    if email == email_to_be_deleted:
                                        del accounts[website_to_be_deleted][
                                            email_to_be_deleted
                                        ]
                                        print("  deleted successfully")
                                        ut.save_accounts(accounts)
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
                        ut.save_accounts(accounts)
                        return
                continue
            print(" website not found ")
    else:
        print("\n No available accounts")


def view_accounts(total_accounts):
    if total_accounts == {}:
        print("No account found\n   press 1 to add Account")
        return
    ut.display_websites_emails(total_accounts)


def load_encrypted_file(cipher_suite):

    try:
        with open("encrypted_data.bin", "rb") as file:
            encrypted_bytes = file.read()  # returns binary data of the encryptee file
            return encrypted_bytes
    except FileNotFoundError:
        accounts = {}  # make encrypted file that store empty dictionary
        encrypted_bytes = make_encrypted_file(cipher_suite, accounts)
        return encrypted_bytes
    except PermissionError:
        print("you do not have permission to access the encrypted_data.bin file")


def load_accounts():
    key = load_key()  # access the key or make the key if not present
    cipher_suite = Fernet(key)  # use the key to encrypt and decrypt stored accounts

    encrypted_bytes = load_encrypted_file(cipher_suite)

    accounts = decrypt_to_dict(cipher_suite, encrypted_bytes)
    return accounts


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
