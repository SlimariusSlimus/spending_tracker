# Spending Tracker Application

A command-line program for tracking spending. It includes basic user account management, purchase logging, and generating financial reports. The project was built as part of a programming course to demonstrate Python fundamentals, file handling, and input validation.

**Note:** Passwords are stored in plain text. This is not secure and the program should not be used for real-world account or financial management. It is intended solely as a programming exercise.

## Features

* **User Accounts:**
    * **Registration:** Create a new account with a username, password, and unique email address. (Passwords are stored in plain text and are not secure.)
    * **Login:** Sign in to an account with a limited number of attempts.

* **Purchase Tracking:**
    * **Log Purchases:** Record details for each item, including seller, date, item name, cost, shipping fees, weight, and quantity.
    * **Spending Limits:** Set a personal financial limit.

* **Reports:**
    * **Full Summary:** Shows all purchases with total spending, total weight, and identifies the most expensive and heaviest items.
    * **Filtered Views:** Generate reports by seller, date, or specific item.

---

## Getting Started

1. **Requirements:**
    * Python 3.x

2. **Run the Application:**
    From the application directory, run:
    ```bash
    python spending_tracker.py
    ```

---

### Core Components

* **Constants & Global Variables:** Store application settings and track the logged-in user.
* **Initialization:** Loads a list of common passwords at startup. Includes error handling for file access issues.

### Decorators

* `@encase_output`: Adds a border around console output for consistent formatting.
* `@requires_login`: Ensures certain functions only run when a user is logged in.

### Functions

* **Utility:** Functions for exiting the program (`exit_program`), formatted printing (`encased_print`), and managing user data files (`load_user_data`, `save_user_data`).
* **Input Validation:** Functions such as `is_valid_new_username`, `is_valid_password`, `is_valid_email`, `is_valid_phone_number`, and `validate_date` check input using regular expressions and logical rules.
* **User Management:** Includes account creation (`register`, `add_user`), authentication (`is_correct_password`, `login`).
* **Purchase Management:** `save_purchase` and `enter_purchase` handle adding new purchases.
* **Reporting:** `generate_full_report`, `generate_filtered_report`, `filter_menu`, and `generate_report` produce summaries and filtered reports.
* **Menus:** `create_dynamic_menu` builds text-based navigation menus.
* **Settings:** `set_spending_limit` updates the spending limit.

---

### Data Storage

All data is stored in **`user_data.json`**. The `json` module is used to convert between Python objects and JSON format for saving and loading.
Passwords are stored in clear text and not encrypted.
