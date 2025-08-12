"""
Menu handling utilities for interactive command-line applications.

Provides functions to display numbered menus, capture and validate user input
and execute corresponding functions. Supports navigation commands for returning
to previous menus and exiting the program.
"""
from typing import List, Dict, Any, Tuple, Callable, Optional, Union
from helpers import exit_program, encased_print


def display_menu(menu_options: List[Tuple[int, Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]]) -> None:
    """
    Prints a list of numbered menu options to the console.

    Displays each option's number and description, followed by a prompt
    indicating how to return to a previous menu.

    Parameters:
        menu_options (List[Tuple[int, Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]]):
            List of menu entries. Each entry consists of:
                - Position number (int)
                - Tuple containing:
                    (callable, description text, positional args tuple, keyword args dict)
    """
    for position, (_, description, _, _) in menu_options:
        print(f'Enter {position} to {description}.')
    print('Enter "back" or "b" to navigate back')


def get_user_choice(valid_positions: List[int]) -> int | str:
    """
    Prompts the user to select a menu option and validates the input.

    Accepts either a valid menu number, or special commands:
        - 'back' or 'b' to return to the previous menu.
        - 'quit', 'q', 'exit', or 'e' to terminate the program.

    Parameters:
        valid_positions (List[int]): List of valid numeric menu choices.

    Returns:
        int | str: The selected menu position as an integer, or a string command.
    """
    while True:
        user_input = input("\nEnter your choice: ").strip().lower()    
        if user_input in {'back', 'b'}:
            return user_input
        elif user_input in {'quit', 'q', 'exit', 'e'}:
            exit_program()
        try:
            choice = int(user_input)
            if choice in valid_positions:
                return choice
            else:
                raise ValueError
        except ValueError:
            encased_print('Invalid input. Please enter a valid number or command.')
        
 
def execute_menu_action(choice: int, menu_options: List[Tuple[int, Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]]) -> Any:
    """
    Executes the function associated with the chosen menu position.

    Searches the provided menu options for the given choice and calls
    the corresponding function with its stored arguments.

    Parameters:
        choice (int): Menu position to execute.
        menu_options (List[Tuple[int, Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]]):
            List of menu entries with callable functions and their arguments.

    Returns:
        Any: The return value from the executed function.
    """
    print()
    for position, (function, _, args, kwargs) in menu_options:
        if choice == position:
            return function(*args, **kwargs)
        
    
def create_dynamic_menu(labeled_funcs: List[Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]) -> Any: 
    """
    Builds and runs a dynamic menu from a list of labeled functions.

    Automatically assigns numeric positions to each provided function,
    adds an exit option, and loops until the user chooses to go back or exit the program.
    Executes the selected function with its stored arguments.

    Parameters:
        labeled_funcs (List[Tuple[Callable[..., Any], str, Tuple[Any, ...], Dict[str, Any]]]):
            Functions to include in the menu, each with a description, positional args, and keyword args.

    Returns:
        Any: The result from the executed menu function.
    """
    menu_options = [(0, (exit_program, 'exit', (), {}))]
    menu_options.extend(enumerate(labeled_funcs, start=1))
    valid_positions = [position[0] for position in menu_options]
    
    while True:
        display_menu(menu_options)
        choice = get_user_choice(valid_positions)
        if choice in {'back', 'b'}:
            break
        result = execute_menu_action(choice, menu_options)
        return result