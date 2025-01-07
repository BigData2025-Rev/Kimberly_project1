import pandas as pd
from pandas.api.types import is_string_dtype
import tabulate
import os

WRAP_WIDTH = 40

#pd.set_option('display.max_colwidth', 20)
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS/Linux
        os.system('clear')

# Displays a list of options to the user and returns the index of the selected option
def options_prompt(options : list[str], prompt : str, clear = True) -> int:
    if clear:
        clear_screen()
    print(prompt)
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if choice < 1 or choice > len(options):
                raise ValueError
            return choice - 1
        except ValueError:
            print("Invalid input. Please enter a number between 1 and", len(options))


# Displays a table of data to the user
# Only use this for small tables
def print_table(data : list[dict]):
    clear_screen()
    if len(data) == 0:
        print("No data found.")
    else:
        df = pd.DataFrame(data)
        for col in df.columns:
            if is_string_dtype(df[col]):
                df[col] = df[col].str.wrap(WRAP_WIDTH)

        if 'description' in df.columns:
            df = df.drop(columns=['description'])
        print(tabulate.tabulate(df, headers='keys', tablefmt='grid'))
    input("Hit enter to continue")
    clear_screen()

# Displays a table of data to the user, with options to navigate to the next or previous page
# Returns -1 for previous, 0 for exit, 1 for next
def print_table_paged(data : list[dict], has_next = False, has_prev = False):
    clear_screen()
    if len(data) == 0:
        print("No data found.")
    else:
        df = pd.DataFrame(data)
        for col in df.columns:
            if is_string_dtype(df[col]):
                df[col] = df[col].str.wrap(WRAP_WIDTH)

        if 'description' in df.columns:
            df = df.drop(columns=['description'])

        print(tabulate.tabulate(df, headers='keys', tablefmt='grid'))

    options = ["Exit"]
    if has_next:
        options.insert(0, "Next page")
    if has_prev:
        options.insert(0, "Previous page")
    selected = options_prompt(options, "Enter selection: ", clear = False)

    if options[selected] == "Next page":
        return 1
    elif options[selected] == "Previous page":
        return -1
    else:
        return 0
    
