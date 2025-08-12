from typing import List, Dict, Any, Tuple, Callable, Optional, Union
from functools import wraps
from datetime import datetime
from helpers import exit_program, encased_print
from create_dynamic_menu import create_dynamic_menu as menu
import json
import re
import time

# -------------------------------------
# |-- Constants & global Variables  --|
# -------------------------------------
APP_NAME = 'Spending Tracker'
USER_DATA_PATH = 'user_data.json'
RESERVED_USERNAMES = {'admin', 'root', 'guest'}
COMMON_PASSWORDS_PATH = '100k-most-used-passwords-NCSC.txt'
COMMON_PASSWORDS = set()

current_user: Dict[str, Any] = None
is_logged_in: bool = False


# ----------------------
# |-- Initialization --|
# ----------------------
try:
    with open(COMMON_PASSWORDS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            COMMON_PASSWORDS.add(line.strip())
except FileNotFoundError:
    print(f'Error: The file "{COMMON_PASSWORDS_PATH}" was not found.')
except PermissionError:
    print(f'Error: Permission denied to read the file "{COMMON_PASSWORDS_PATH}".')
except IOError as e:
    print(f'Error: An I/O error occurred while reading "{COMMON_PASSWORDS_PATH}": {e}')
except Exception as e:
    print(f'An unexpected error occurred while trying to read data from "{COMMON_PASSWORDS_PATH}": {e}')


# ------------------
# |-- Decorators --|
# ------------------
def encase_output(symbol: str = '-', length: int = 70) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator that prints a separator before and after the decorated function's execution.

    Parameters:
        symbol (str): The character used for the separator.
        length (int): The length of the separator line.
    """
    # for decorators that can accept arguments, we need a seccond decoratpor
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(symbol * length)
            function = func(*args, **kwargs)
            print(symbol * length)
            return function
        return wrapper
    return decorator


def requires_login(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that checks whether the user is logged in before executing the function.

    If the user is not logged in, it prints a message and prevents the decorated function from running.

    Parameters:
        func (Callable[..., Any]): The function to decorate.
        *args (Any): Positional arguments (unused by the decorator directly).
        **kwargs (Any): Keyword arguments (unused by the decorator directly).

    Returns:
        Callable[..., Any]: A wrapped version of the original function that enforces login status.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not is_logged_in:
            encased_print('You have to be logged in for that!')
            return None
        return func(*args, **kwargs)
    return wrapper

# -----------------
# |-- Functions --|
# -----------------

def load_user_data(*, data_path: str = USER_DATA_PATH) -> List[Dict[str, Any]]:
    """"
    Load and return user data from a json file, expecting a list of dictionaries inside.
    
    Parameters:
        data_path (str)
    
    Returns:
        user_data (List[Dict[str, Any]])
    
    """
    try:    
        with open(data_path, 'r') as f:
            users = json.load(f)
        return users
    except PermissionError as e:
        print('Error: Permission denied to read the file.')
    except FileNotFoundError as e:
        print(f'Error: The file {data_path} does not exist.')
    except IOError as e:
        print(f'Error: An I/O error occurred while reading "{data_path}": {e}')
    except json.JSONDecodeError as e:
        print(f'Error: Could not decode JSON from "{data_path}". The file might be corrupted or not valid JSON.')
    except Exception as e:
        print(f'An unexpected error occurred while trying to read data from "{data_path}": {e}')
    
  
def save_user_data(users: List[Dict[str, Any]]) -> None:
    """
    Writes the entire list of user records to disk in JSON format.

    Handles file I/O and JSON serialization errors gracefully, printing appropriate messages.

    Parameters:
        users (List[Dict[str, Any]]): The complete list of user data to be saved.
    """
    try:
        with open(USER_DATA_PATH, 'w') as f:
            json.dump(users, f, indent=2)
        encased_print(f'Successfully saved new data to file {USER_DATA_PATH}!')
    except IOError as e:
        print(f'Error writing to file "{USER_DATA_PATH}": {e}')
    except TypeError as e:
        print(f'Error serializing data to JSON: {e}')
    except Exception as e:
        print(f'An unexpected error occurred while trying to save user data: {e}')
        
        
def is_valid_new_username(username: str, users: List[Dict[str, Any]]) -> bool: 
    """
    Check if a given username is valid and not already in use.

    A valid username:
    - Contains only lowercase letters, digits, hyphens, or underscores
    - Is between 3 and 14 characters long
    - Is not in the reserved usernames list
    - Does not already exist in the provided users list

    Parameters:
        username (str): The username to check.
        users (List[Dict[str, Any]]): This is the user data

    Returns:
        bool: True if the username is valid and unused, False otherwise.
    """
    if not re.fullmatch(r'^[a-z0-9_-]{3,14}$', username):
        encased_print(
            f'"{username}" is not a valid username!',
            'Username must be 4-14 characters long and contain only lowercase letters, digits, hyphens (-), or underscores (_).',
            'Please try again.'
        )
        return False
    elif username in RESERVED_USERNAMES:
        encased_print(f'Username "{username}" already exists! Please try again.')
        return False
    else:
        for user in users:
            if user['username'] == username:
                encased_print(f'Username "{username}" already exists! Please try again.')
                return False
    return True
    
    
def is_valid_password(password: str) -> bool:
    """
    Validate a password against a set of security rules.

    A valid password must:
    - Be 8 to 20 characters long
    - Contain at least one uppercase letter, lowercase letter, digit and special character (!@#$%^&*)
    - Not contain spaces
    - Not be in the list of the 100,000 most common passwords

    Parameters:
        password (str): The password to validate.

    Returns:
        bool: True if the password meets all criteria, False otherwise.
    """
    pattern_upper = r'[A-Z]'
    pattern_lower = r'[a-z]'
    pattern_digit = r'\d'
    pattern_special = r'[!@#$%^&*]'
    pattern_space = r' '
    reasons = []
    if password in COMMON_PASSWORDS:
        reasons.append('not be too common')
    if re.search(pattern_space, password):
        reasons.append('not contain empty spaces')
    if not (8 <= len(password) <= 20):
        reasons.append('be between 8 and 20 characters long')
    if not re.search(pattern_upper, password):
        reasons.append('contain at least one uppercase letter')
    if not re.search(pattern_lower, password):
        reasons.append('contain at least one lowercase letter')
    if not re.search(pattern_digit, password):
        reasons.append('contain at least one digit')
    if not re.search(pattern_special, password):
        reasons.append('contain at least one special character')
    if not reasons:
        return True
    encased_print(f'"{password}" is an invalid password.\nPassword must:\n- {',\n- '.join(reasons)}')
    return False


def is_valid_email(email: str, users: List[Dict[str, Any]]) -> bool:  
    """
    Validate an email address for correct format and uniqueness.

    An email is considered valid if:
    - It matches a basic pattern (text@text.domain)
    - It is not already used by an existing user in the given list

    Parameters:
        email (str): The email address to validate.
        users (List[Dict[str, Any]]): List of existing users with an 'email' field.

    Returns:
        bool: True if the email is valid and unused, False otherwise.
    """
    if not re.fullmatch(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+', email):
        encased_print('Invalid email format. Please try again.')
        return False
    elif email in [user['email'] for user in users]:
        encased_print(f'A user with the e-mail address "{email}" already exists! Please try again.')
        return False
    return True


def is_valid_phone_number(phone_number: str) -> bool:
    """
    Validate an international phone number in E.164 format.

    A valid phone number:
    - Starts with a '+' followed by 8 to 15 digits
    - Contains no spaces, dashes, or other characters

    Parameters:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    if not re.fullmatch(r'^\+\d{8,15}$', phone_number):
        encased_print('Invalid phone number format. Please try again.')
        return False
    return True


def validate_date(date_input: str) -> Optional[str]:
    """
    Validates and reformats a user-provided date string.

    Accepts input in either "MM/DD/YYYY" or "MM-DD-YYYY" format. If the input matches one of these formats, returns the date
    reformatted as "YYYY/MM/DD". If the input is invalid, prints an error message and returns None.

    Parameters:
        date_input (str): The date string provided by the user.

    Returns:
        Optional[str]: Reformatted date string in "YYYY/MM/DD" format
                       if valid, otherwise None.
    """
    allowed_formats = {"%m-%d-%Y", "%m/%d/%Y"}
    saving_format = '%Y/%m/%d'
    for format_ in allowed_formats: 
        try: 
            date = datetime.strptime(date_input, format_).strftime(saving_format) # correctly formatted date string
            return date
        except ValueError:
            pass
    encased_print('Invalid date format. Provide in either "MM/DD/YYYY" or "MM-DD-YYYY".', 'Please try again.')
    
    
def register(users: List[Dict[str, Any]]) -> None:
    """
    Interactively collect and validate user input to register a new user.

    Prompts for a username, password, email, and phone number.  
    Each field is validated using its corresponding validation function.  
    If all fields are valid, the new user is added to the user list and saved.

    Parameters:
        users (List[Dict[str, Any]]): The user data.

    Returns:
        List[Dict[str, Any]]: Updated user data including the new user.
    """
    new_user = {}
    print('Register new user')
    while True:
        username = input('Please enter your desired username: ').strip()
        if is_valid_new_username(username, users):
            break
    while True:
        password = input('Please enter your Password: ').strip()
        if is_valid_password(password):
            repeated_password = input('Please enter your Password again: ').strip()
            if repeated_password == password:
                break
    while True:
        email = input('Please enter your E-Mail address: ').strip()
        if is_valid_email(email, users):
            break
    while True:
        phone_number = input('Please enter your phone number in this format: +491234567890 : ').strip()
        if is_valid_phone_number(phone_number):
            break
    while True:
        try:
            spending_limit = float(input('Please enter a spending limit in €. You can change it later. : ').strip())
            if not spending_limit:
                spending_limit = 0
            break
        except ValueError:
            encased_print('Not a valid number! Please try again.')
            
    new_user['username'] = username
    new_user['password'] = password
    new_user['email'] = email
    new_user['phone'] = phone_number
    new_user['purchases'] = []
    new_user['spending_limit'] = spending_limit
    add_user(new_user, users)
    

def add_user(new_user: Dict[str, Any], users: List[Dict[str, Any]]) -> None:
    """
    Adds a new user to the list of users and persists the updated data to disk.

    Delegates the actual saving to `save_user_data`.

    Parameters:
        new_user (Dict[str, Any]): The user data to append.
        users (List[Dict[str, Any]]): The list of all existing users.
    """
    users.append(new_user)
    save_user_data(users)
    encased_print(f'Successfully registered new user {new_user['username']}!')


def is_correct_password(user_data: Dict[str, Any]) -> bool:
    """
    Prompt the user up to three times to enter the correct password.

    Compares the input with the stored password in user_data.
    Returns after first match or after three failed attempts.

    Parameters:
        user_data (Dict[str, Any]): The data of the user in the original user data.

    Returns:
        bool: True if the correct password was entered, False otherwise.
    """
    MAX_PASSWORD_ATTEMPTS = 3
    for i in range(MAX_PASSWORD_ATTEMPTS):
        password = input('Please enter your password: ').strip()
        if user_data['password'] == password:
            return True
        print('Wait 5 seconds to retry')
        time.sleep(5)
    exit_program('Too many unsuccessful login attempts')


def login(users: List[Dict[str, Any]]) -> bool:
    """
    Authenticate a user by username and password.

    Prompts for username and checks if it exists in the given user list.
    If found, prompts for the password with up to three attempts.
    Prints login result.

    Parameters:
        users (List[Dict[str, Any]]): List of user dictionaries with at least 'username' and 'password' keys.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    global current_user, is_logged_in
    if is_logged_in:
        encased_print('You\'re already logged in')
        return False
    user_data = None
    username = input('Please enter your username: ').strip()
    for user in users:
        if user['username'] == username:
            user_data = user
            break
    if user_data:
        if is_correct_password(user_data):
            current_user = user_data
            is_logged_in = True
            encased_print(f'\nWelcome, {username}! Login successful!')
            return True
    encased_print('Incorrect login credentials!')
    current_user = None # Just to be sure
    is_logged_in = False
    return False

  
@requires_login   
def save_purchase(purchase_data: Dict[str, Any], users: List[Dict[str, Any]]) -> bool:
    """
    Saves a validated purchase entry to the current user's purchase history and 
    calls the save_user_data function to write the updated data to disk.

    Parameters:
        purchase_data (Dict[str, Any]): The purchase information to store.
        users (List[Dict[str, Any]]): The list of all user records to be updated and written to file.

    Returns:
        bool: True if the purchase is saved and data written successfully.
    """
    current_user['purchases'].append(purchase_data)
    save_user_data(users)
    encased_print(f'Saved purchase from {purchase_data['date']} successfully!')
    return True


@requires_login
def enter_purchase(users: List[Dict[str, Any]]) -> None:
    """
    Interactive input loop to collect and validate purchase data from the user.

    On successful validation, displays a purchase summary and prompts the user to confirm saving.
    If confirmed, passes the data to `save_purchase`.

    Parameters:
        users (List[Dict[str, Any]]): The list of all user records used for saving the updated purchase.
    """
    while True:
        while True:
            seller = input('Where did you buy the product? (Amazon, Ebay, Temu, etc...): ').strip().lower()
            if len(seller) >= 3:
                break
            encased_print('Seller name should be at least 3 characters. Please try again.')
        while True:
            date_input = input('When did you buy the product? (MM/DD/YYYY or MM-DD-YYYY): ').strip()
            if validate_date(date_input):
                date = date_input
                break
        while True:
            item = input('What\'s the name of the item you bought?: ').strip().lower()
            if len(item) >= 3:
                break
            encased_print('Item name should be at least 3 characters. Please try again.')
        while True:
            try:
                cost = float(input('How much did it one unit cost? (in EUR): ').strip())
                break
            except ValueError:
                encased_print('Not a valid number!\nPlease try again')
        while True:
            try:
                delivery_fee = float(input('How much was the delivery fee? (in EUR): ').strip())
                break
            except ValueError:
                encased_print('Not a valid number! (example: 2.4)\nPlease try again')
        while True:
            try:
                weight = float(input('How much does one unit weigh? (in kg): ').strip())
                break
            except ValueError:
                encased_print('Not a valid number!\nPlease try again')
        while True:
            try:
                quantity = int(input('How many units did you buy?: ').strip())
                break
            except ValueError:
                encased_print('Not a valid number!\nPlease try again')
        total_weight = quantity * weight
        total_cost = quantity * cost + delivery_fee
        purchase_data = {
            'date': date,
            'seller': seller,
            'item_name': item,
            'cost' : cost,
            'quantity': quantity,
            'total_weight': total_weight,
            'total_cost': total_cost
        }
        if purchase_data in current_user['purchases']:
            encased_print('This purchase data already exists!')
            break
        encased_print(
            f'Here\'s a summary of your purchase:',
            purchase_data,
            f'Are you sure, you want to save this purchase?'
            )
        user_confirmation = [
                (save_purchase, 'save data', (purchase_data, users), {}),
                (lambda: False, 'enter data again', (), {}),
            ]
        if menu(user_confirmation):
            break

@encase_output()
@requires_login   
def generate_full_report(purchases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates and displays a full summary report of all purchases by the current user.

    Reports include total spending, total weight, and highlight the most expensive and heaviest purchases.

    Parameters:
        purchases (List[Dict[str, Any]]): The user's full list of purchase records.
        
    Returns:
        purchases (List[Dict[str, Any]]): A List of all purchases done by the user.
    """
    priciest_purchase = max(purchases, key=lambda purchase: purchase["total_cost"])
    heaviest_purchase = max(purchases, key=lambda purchase: purchase["total_weight"])
    total_spending = sum(purchase['total_cost'] for purchase in purchases)
    total_weight = sum(purchase['total_weight'] for purchase in purchases)
    total_quantity = sum(purchase['quantity'] for purchase in purchases)
    total_purchases = len(purchases)
    print('Here is a summary of your previous purchases:\n')
    print(f'You bought {total_quantity} items for a total of: {total_spending:.2f}€.')
    print(f'With a total weight of: {total_weight:.2f} kg.')
    print()
    print(f'Your most expensive purchase was: {priciest_purchase['quantity']} {priciest_purchase['item_name']} at {priciest_purchase['seller']}')
    print(f'for a total of {priciest_purchase['total_cost']:.2f}€.')
    print()
    print(f'Your heaviest purchase was: {heaviest_purchase['quantity']} {heaviest_purchase['item_name']} at {heaviest_purchase['seller']}')
    print(f'for a total of {heaviest_purchase['total_weight']:.2f} kg.')
    print()
    print(f'You did a total of {total_purchases} purchases for a total of {total_quantity} items.')
    print(f'On average you spent {total_spending / total_purchases:.2f}€ per purchase and {total_spending / total_quantity:.2f}€ per item.')
    spending_limit = current_user['spending_limit']
    if spending_limit:
        limit_diff = current_user['spending_limit'] - total_spending
        if limit_diff == 0:
            print(f'You have hit your set limit of {current_user['spending_limit']}€!')
        elif limit_diff < 0:
            print(f'You have exceeded your set limit of {spending_limit}€ by {abs(limit_diff):.2f}!€')
        else:
            print(f'You have {abs(limit_diff):.2f}€ left before reaching your set limit of {spending_limit:.2f}€!')
    return purchases


@encase_output()
@requires_login
def generate_filtered_report(purchases: List[Dict[str, Any]], filter_key: str) -> List[Dict[str, Any]]:
    """
    Generates a filtered report of purchases based on a user-specified field and value.

    Displays total spending, total weight, and highlights the most expensive and heaviest purchases
    that match the given filter.

    Parameters:
        purchases (List[Dict[str, Any]]): The user's list of purchase records to filter.
        filter_key (str): The field to filter by, e.g., "seller", "date", or "item".
        
    Returns:
        purchases (List[Dict[str, Any]]): A List of all purchases done by the user, matching the filter.
    """
    if filter_key not in set(purchases[0].keys()):
        print('Invalid filter key!')
        return
    while True:
        filter_key_value = input(f'Please enter the {filter_key} you want to filter for: ').lower()
        if filter_key == 'date':
            if not validate_date(filter_key_value):
                continue
        break
    filtered_purchases = [purchase for purchase in purchases if purchase[filter_key] == filter_key_value]
    if not filtered_purchases:
        print(f"No purchases found matching filter: {filter_key} = {filter_key_value.capitalize()}")
        return
    priciest_purchase = max(filtered_purchases, key=lambda purchase: purchase["total_cost"])
    heaviest_purchase = max(filtered_purchases, key=lambda purchase: purchase["total_weight"])
    total_spending = sum(purchase['total_cost'] for purchase in filtered_purchases)
    total_weight = sum(purchase['total_weight'] for purchase in filtered_purchases)
    total_quantity = sum(purchase['quantity'] for purchase in filtered_purchases)
    total_purchases = len(filtered_purchases)
    print(f'Here is a summary of your previous purchases, filtered for {filter_key} = {filter_key_value}:\n')
    print(f'You bought {total_quantity} items for a total of: {total_spending:.2f}€.')
    print(f'With a total weight of: {total_weight:.2f} kg.')
    print()
    print(f'Your most expensive purchase was: {priciest_purchase['quantity']} {priciest_purchase['item_name']} at {priciest_purchase['seller']}')
    print(f'for a total of {priciest_purchase['total_cost']:.2f}€.')
    print()
    print(f'Your heaviest purchase was: {heaviest_purchase['quantity']} {heaviest_purchase['item_name']} at {heaviest_purchase['seller']}')
    print(f'for a total of {total_weight:.2f} kg.')
    print()
    print(f'You did a total of {total_purchases} purchases, for a total of {total_quantity} items.')
    print(f'On average you spent {total_spending / total_purchases:.2f}€ per purchase')
    print(f'and {total_spending / total_quantity:.2f}€ per item.')
    return filtered_purchases


@requires_login   
def filter_menu(purchases: List[Dict[str, Any]]) -> None:
    """
    Displays a menu to let the user choose a filter type for generating a filtered purchase report.

    Passes the chosen filter type to `create_filtered_report`.

    Parameters:
        purchases (List[Dict[str, Any]]): The user's list of purchase records.
    """
    filtered_menu_options = [
        (generate_filtered_report, 'filter for seller', (purchases, 'seller'), {}),
        (generate_filtered_report, 'filter for date', (purchases, 'date'), {}),
        (generate_filtered_report, 'filter for item', (purchases, 'item_name'), {})
    ]
    return menu(filtered_menu_options)


@requires_login
def generate_report(report_type: str = '') -> None:
    """
    Controls generation of reports for the current user.

    If no type is specified, displays a menu offering 'full' or 'filtered' report options.
    Delegates report creation to `create_full_report` or `filter_menu` accordingly.

    Parameters:
        report_type (str): Either "full", "filtered", or empty string to trigger the selection menu.
    """
    report_options = [
            (generate_report, 'create full report', ('full', ), {}),
            (generate_report, 'create a filtered report', ('filtered', ), {})
        ]
    purchases = current_user.get('purchases', [])
    output_purchases = None
    if not report_type:
        print('What kind of report do you want?')
        menu(report_options)
    elif report_type == 'full':
        output_purchases = generate_full_report(purchases)
    elif report_type == 'filtered':
        output_purchases = filter_menu(purchases)
    if output_purchases:
        encased_print('Do you want a list of all the purchases?')
        user_decision = [
            (lambda data=output_purchases: data, 'show list', (output_purchases, ), {}),
            (lambda: None, 'end the report', (), {})
        ]
        purchase_list = menu(user_decision)
        # if len(purchase_list) is 5, max_digits will be 1 (for for len(4))
        # if len(purchase_list) is 15, max_digits will be 2 (for len(14))
        max_digits = len(str(len(purchase_list) - 1))
        if purchase_list:
            for i, purchase in enumerate(purchase_list):
                print(f'[{i:0{max_digits}}] {purchase}')
                
                

   
            
      
@requires_login 
def set_spending_limit(users: List[Dict[str, Any]]) -> None:
    while True:
        try:
            limit = float(input('What do you want your limit to be?: ').strip())
            break
        except ValueError:
            encased_print('Please enter a valid number! Please try again.')
    current_user['spending_limit'] = limit
    save_user_data(users)
    print(f'Spending limit set to {limit:.2f}€.')
    

def main():
    users = load_user_data()
    print('-'*40)
    print(f'|   Welcome to the {APP_NAME}!   |')
    print('-'*40)
    # loop for the main menu
    while True:
        user_control_actions = [
            (login, 'login', (users,), {}),
            (register, 'register', (users,), {})
        ]
        user_spending_actions = [
            (enter_purchase, 'enter a new purchase', (users, ), {}),
            (generate_report, 'generate a report of your current spending', (), {}),
            (set_spending_limit, 'set a custom spending limit', (users, ), {})
        ]
        top_level_menu_options = [
                (menu, 'login / register', (user_control_actions,), {}),
                (menu, 'manage your purchases', (user_spending_actions,), {})
            ]
        if is_logged_in:
            top_level_menu_options = [
                (menu, 'manage your purchases', (user_spending_actions,), {})
            ]
        menu(top_level_menu_options)
        

if __name__ == "__main__":
    main()