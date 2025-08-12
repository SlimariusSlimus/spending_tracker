"""
Colection of small functions to help handle simple things
"""
from typing import List, Dict, Any, Tuple, Callable, Optional, Union
from functools import wraps
import sys


def exit_program(*, reason: str | None = None) -> None:
    """
    Terminates the program gracefully after optional user notification.

    Displays a termination message, optionally followed by a provided reason,
    then waits for the user to press Enter before exiting.

    Parameters:
        reason (str | None): Optional explanation for why the program is ending.
    """
    print('The program has ended.')
    if reason:
        print('This was for the following reason:')
        print(f'{reason}\n')
    input('Press Enter to exit...')
    sys.exit()
    
    
def encased_print(*args: Any, symbol: str = '-', length: int = 70) -> None:
    """
    Prints text enclosed within a repeated symbol border.

    Each argument is printed on a separate line, framed above and below
    by a horizontal line composed of the specified symbol.

    Parameters:
        *args (Any): Values to print, each on a separate line.
        symbol (str): Character to use for the border (default '-').
        length (int): Number of symbols to repeat for the border (default 70).
    """
    print(symbol * length)
    if not args:
        print()
        return
    for arg in args:
        print(arg)
    print(symbol * length)
    