# Spending Tracker Application

This command-line application offers a straightforward way to keep tabs on spending. It provides functionalities for user management, purchase logging, and generating various financial reports. This project was built as part of a programming course, highlighting core Python concepts, file handling, and robust input validation.

## Features

* **User Accounts:**
    * **Registration:** Create a new account with a secure username and strong password, along with a unique email address. (please mind that passwords are not encrypted and therefore not secure!)
    * **Login:** Access your account, with a limited number of attempts to ensure security.

* **Purchase Tracking:**
    * **Log Purchases:** Easily record details for each item, including where it was bought, the date, item name, cost, shipping fees, weight, and quantity.
    * **Spending Limits:** Set a custom financial limit to help manage your budget effectively.

* **Detailed Reports:**
    * **Full Summary:** Get a complete overview of all your purchases, showing total spending, total weight, and highlighting your most expensive and heaviest buys.
    * **Filtered Views:** Generate specialized reports based on criteria like seller, date, or specific items.

---

## Getting Started

1.  **Requirements:**
    * Python 3.x installed on your system.

2.  **Run the Application:**
    Navigate to the application's directory in your terminal or command prompt and execute:
    ```bash
    python spending_tracker.py
    ```

---

### Core Components

* **Constants & Global Variables:** These define essential settings and track the application's overall state, like the currently logged-in user.
* **Initialization:** At startup, the application attempts to load a list of common passwords. Comprehensive **error handling** is in place to gracefully manage any issues during file access, such as a missing file or permission problems.

### Enhancing Functionality with Decorators

* `@encase_output`: This decorator frames console output with a consistent visual border, making messages stand out.
* `@requires_login`: A crucial decorator that ensures sensitive functions only run when a user is properly logged in, protecting user data.

### Well-Defined Functions

The codebase is broken down into small, purposeful functions, each designed for a specific task.

* **Utility Functions:** These handle common operations like ending the program (`exit_program`), formatting print statements (`encased_print`), and managing user data files (`load_user_data`, `save_user_data`).
* **Input Validation:** Functions such as `is_valid_new_username`, `is_valid_password`, `is_valid_email`, `is_valid_phone_number`, and `validate_date` rigorously check user input. They use **regular expressions** and logical checks to ensure data is correct and secure, enforcing rules like password complexity.
* **User Management:** This set of functions (`register`, `add_user`, `is_correct_password`, `login`) manages the entire user lifecycle, from account creation to authentication.
* **Purchase Management:** `save_purchase` and `enter_purchase` facilitate the interactive process of recording and storing new purchases.
* **Reporting:** `generate_full_report`, `generate_filtered_report`, `filter_menu`, and `generate_report` provide flexible ways to analyze spending data, offering both comprehensive summaries and focused reports.
* **Interactive Menus:** The `create_dynamic_menu` function is key to the application's user interface. It constructs interactive menus based on a list of available actions, making navigation intuitive.
* **Settings:** `set_spending_limit` allows users to easily adjust their financial goals within the application.

---

### Data Handling and Persistence

All user information and purchase records are stored persistently in a **`user_data.json`** file. The application uses Python's `json` module to handle the seamless conversion of data between Python objects and JSON format, ensuring that your financial records are saved and retrieved correctly across sessions.
