# 🔐 CLI Password Manager

A secure command-line password manager built in **Python**. This project stores account credentials locally in an encrypted file and allows users to manage passwords through an interactive terminal interface.

## Features

* Add new website accounts
* Store multiple email accounts under the same website
* Search for passwords by website
* Update existing passwords
* Delete individual accounts or entire websites
* Generate cryptographically secure random passwords
* Encrypt and decrypt stored data
* Automatic saving after every modification
* Input validation and error handling
* Modular project structure

## Technologies Used

* Python 3
* JSON
* `secrets` module
* `cryptography` (Fernet)
* File Handling

## Data Structure

Accounts are stored in a nested dictionary.

```python
{
    "github": {
        "personal@gmail.com": {
            "Password": "********"
        },
        "work@gmail.com": {
            "Password": "********"
        }
    },
    "google": {
        "example@gmail.com": {
            "Password": "********"
        }
    }
}
```

This structure allows:

* Multiple email accounts per website
* Fast website lookup
* Easy password updates
* Simple account deletion

## How Encryption Works

1. The account dictionary is converted into a JSON string.
2. The JSON string is converted into bytes.
3. The bytes are encrypted using a generated encryption key.
4. The encrypted data is saved to `stored_accounts.bin`.
5. When the program starts, the encrypted file is decrypted and loaded back into memory.

> **Note:** The encryption key is stored locally and excluded from Git using `.gitignore`.

## Random Password Generator

The application can generate strong passwords using Python's `secrets` module.

Features:

* User chooses password length
* Minimum length validation
* Uses printable ASCII characters (excluding problematic characters such as `\`)

## Program Workflow

```text
Start Program
      │
      ▼
Load Encrypted Database
      │
      ▼
Decrypt Data
      │
      ▼
Load Accounts into Memory
      │
      ▼
User Performs Operations
      │
      ▼
Save Changes
      │
      ▼
Encrypt Database
      │
      ▼
Exit
```

## Menu

* Add Account
* Search Password
* Update Password
* Delete Account
* Generate Random Password
* Display Stored Websites
* Exit

## Error Handling

The application validates:

* Invalid menu choices
* Non-integer input where integers are expected
* Missing websites
* Missing email accounts
* Invalid password generation length
* Empty account database
* Duplicate account handling

## Design Decisions

### Why Nested Dictionaries?

A nested dictionary allows fast access to accounts using:

```
Website → Email → Password
```

This supports multiple email accounts under the same website without unnecessary searching.

### Why Save After Every Modification?

Saving immediately ensures that data is not lost if the application closes unexpectedly.

### Why Use `secrets` Instead of `random`?

`secrets` is designed for generating cryptographically secure random values and is appropriate for password generation, whereas random is predicable.

### Why Separate Encryption Logic?

All encryption and decryption logic is placed in a separate file to keep the code modular and maintainable.

## Future Improvements

* Master password authentication
* Key derivation using Argon2 or PBKDF2
* Store the salt with the encrypted database
* Password strength checker
* Copy password directly to clipboard
* Import/Export encrypted backups
* Password history
* Automatic database backups
* Cross-platform support
* GUI version
* Search by email address
* Password expiration reminders

## What I Learned

Building this project helped me understand:

* Modular software design
* Dictionaries and nested data structures
* JSON serialization
* File handling
* Exception handling
* Input validation
* Encryption fundamentals
* Secure password generation
* Refactoring and code reuse
* Designing software before implementation

## Disclaimer

This project was built for learning software engineering and security fundamentals. While it uses encryption to protect stored data, it is not intended to replace mature password managers without further security auditing and testing.
