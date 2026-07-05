from cryptography.fernet import Fernet
import os
import json

# secret.key stores the key(in bytes) to encrypt and decrypt the data
KEY_FILE = "secret.key"


def load_key():
    # if the file doesn't exists, generate it
    if not os.path.exists(KEY_FILE):
        print("Creating a new local key: ", KEY_FILE)
        new_key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(new_key)
        return new_key

    # if key exists, just read it
    with open(KEY_FILE, "rb") as f:
        return f.read()


def make_encrypted_file(cipher_suite, accounts):
    accounts_in_bytes = json_to_bytes(accounts)
    encrypted_token = cipher_suite.encrypt(accounts_in_bytes)

    with open("encrypted_data.bin", "wb") as data_file:
        encrypted_bytes = data_file.write(encrypted_token)
    return encrypted_bytes


def decrypt_to_dict(cipher_suite, encrypted_bytes):
    decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)
    accounts_in_json = bytes_to_json(decrypted_bytes)
    accounts_in_dictionary = json.loads(accounts_in_json)
    return accounts_in_dictionary


def bytes_to_json(decrypted_bytes):
    accounts_in_json = decrypted_bytes.decode("utf-8")
    return accounts_in_json


def json_to_bytes(accounts):
    # Turn the dictionary into a JSON string, then into bytes
    accounts_in_json = json.dumps(accounts)
    accounts_in_bytes = accounts_in_json.encode("utf-8")
    return accounts_in_bytes
