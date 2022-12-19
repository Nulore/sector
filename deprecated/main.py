from colorama import Fore, Back, Style
from databank import databank, get_item_databank
import stringer
import pyfiglet
import toml

commands = {}

def welcome():
    pyfiglet.print_figlet("AI Query")
    print("direct terminal access to your ship's AI.")
    print(f"type {Style.BRIGHT}{Fore.GREEN}help{Style.RESET_ALL} for a list of commands.")

def print_character(character_dict: dict):
    message = stringer.character(character_dict)
    print(message)

def print_species(arguments):
    species: str = arguments[0]
    message = stringer.species(species)

    print(message)

def print_faction(arguments):
    faction_string: str = arguments[0]
    message = stringer.faction(faction_string)

    print(message)

def print_weapon(arguments):
    weapon: str = arguments[0]
    message = stringer.weapon(weapon)

    print(message)

def register_commands():
    global commands

    class Command():
        def __init__(self, run_callback, help_string: str, requires_arguments = True) -> None:
            self.help_string = help_string
            self.run = run_callback
            self.requires_arguments = requires_arguments

        def help(self):
            print(self.help_string)

        def run(self, arguments):
            pass
    
    def char(arguments):
        try:
            print_character(toml.load(f"crew/{arguments[0]}.toml"))
        except FileNotFoundError:
            print(f"file not found crew/{arguments[0]}.toml")
    
    def list_data(arguments):
        message = []
        try:
            for key in databank[arguments[0]].keys():
                message.append(key)
        except KeyError:
            print(f"{arguments[0]} is not in the databank. these are what you can search:")
            for key in databank.keys():
                message.append(key)
        print(', '.join(message))

    commands = {
        "char": Command(
            char,
            "<character_name>"
        ),
        "spec": Command(
            print_species,
            "<species_name>"
        ),
        "wep": Command(
            print_weapon,
            "<weapon_name>"
        ),
        "fact": Command(
            print_faction,
            "<faction_name>"
        ),
        "list": Command(
            list_data,
            "<bank>"
        )
    }

    print("registered commands.")

def parse(rawcommand: str):
    arguments = rawcommand.split(" ")
    command = arguments.pop(0)
    
    if command == "help":
        if len(arguments) > 0:
            try:
                print(commands[arguments[0]].help_string)
            except KeyError:
                print(f"not a valid command, {arguments[0]}")
        else:
            for command in commands.keys():
                print(f"{command} {commands[command].help_string}")
            print("help <command>")

    elif command in commands.keys():
        if len(arguments) <= 0:
            return print("supply arguments.")
        else:
            commands[command].run(arguments)

    else:
        print(f"command not registered, \"{command}\"")

def main():
    welcome()
    register_commands()
    while True:
        print("")
        query = input(f"{Style.BRIGHT}{Fore.BLUE}> query: {Style.RESET_ALL}")
        if query == "q":
            print("goodbye")
            break
        parse(query)
    
if __name__ == '__main__':
    main()