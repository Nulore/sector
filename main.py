from colorama import Fore, Back, Style
import pyfiglet
import toml

databank = {
    "species": toml.load("databank/species.toml"),
    "weapon": toml.load("databank/weapons.toml"),
    "creature": toml.load("databank/creatures.toml"),
    "disease": toml.load("databank/diseases.toml"),
    "faction": toml.load("databank/factions.toml"),
    "sector": toml.load("databank/sectors.toml"),
}

commands = {}

def welcome():
    pyfiglet.print_figlet("AI Query")
    print("direct terminal access to your ship's AI.")
    print(f"type {Style.BRIGHT}{Fore.GREEN}help{Style.RESET_ALL} for a list of commands.")

def get_item_databank(db: str, item: str):
    return databank[db][item]

def print_character(character_dict: dict):
    name: str = character_dict['meta']['name']
    job: str = character_dict['meta']['occupation']
    species: str = character_dict['meta']['species']

    message = f"""{Style.BRIGHT}{Fore.RED}{name}, {job.lower()} (a {species}){Style.RESET_ALL}
    {databank['species'][character_dict['meta']['species']]['description']}"""
    
    if character_dict['meta']['species'] != "ai":
        message += f"""
{Style.BRIGHT}{Fore.GREEN}HEALTH{Style.RESET_ALL}
{name} is {(character_dict['health']['health'] / (100 + character_dict['health']['armor'])) * 100}% healthy.
{character_dict['health']['health']} HP, {100 + character_dict['health']['armor']} MHP, {character_dict['health']['armor']} armor.

{name} is in {(character_dict['health']['pain'] / 100) * 100}% pain.
{name} has {(character_dict['health']['oxygen'] / 100) * 100}% oxygen."""
    else:
        message += f"""

AI currently has {character_dict['meta']['nodes']:,} nodes.

Biometric print required for AI override code.
Biometrics scanned, welcome Captain.
The {Style.BRIGHT}{Fore.RED}AI override code is{Style.RESET_ALL} {character_dict['meta']['code']}"""
    print(message)

def print_species(arguments):
    species: str = arguments[0]
    message = f"species not found, {species}"
    if species in databank["species"]:
        message = f"""{Style.BRIGHT}{Fore.RED}{databank["species"][species]['plural']} ({databank["species"][species]['single']}){Style.RESET_ALL}
        {databank["species"][species]['description']}"""

    print(message)

def print_faction(arguments):
    faction_string: str = arguments[0]
    message = f"faction not found, {faction_string}"
    if faction_string in databank["faction"]:
        faction = get_item_databank("faction", faction_string)

        enemies = faction["enemies"].split(",")
        allies = faction["allies"].split(",")

        def pretty(array):
            # also todo faction suffixes
            # [
            #     "Vanus",
            #     "Federation",
            #     "Government",
            #     "Union",
            #     "Company",
            #     "Coalition",
            #     "Alliance",
            #     "Syndicate",
            #     "Conglomerate",
            #     "Bond",
            #     "Concord",
            #     "League",
            #     "Nation",
            #     "Glorianis"
            # ]
            # todo fix pirates
            if len(array) < 1:
                return
            
            if array[0] == '':
                array[0] = "None"
                return

            if array[0] == "*":
                array[0] = "All"
            else:
                for i, s in enumerate(array):
                    array[i] = databank["faction"][s]["name"]
        
        pretty(enemies)
        pretty(allies)
        
        message = f"""{Style.BRIGHT}{Fore.RED}{faction['name']}
        {Fore.GREEN}"{faction['motto']}"{Style.RESET_ALL}
{faction['description']}

{Fore.GREEN}Allies:{Style.RESET_ALL} {', '.join(allies)}
{Fore.RED}Enemies:{Style.RESET_ALL} {', '.join(enemies)}
        """


    print(message)

def print_weapon(arguments):
    weapon: str = arguments[0]
    message = f"weapon not found, {weapon}"
    if weapon in databank["weapon"]:
        dweapon = databank["weapon"][weapon]
        message = f"""{Style.BRIGHT}{Fore.GREEN}{dweapon['name']}{Style.RESET_ALL}
    {dweapon['description']}

{Style.BRIGHT}{Fore.GREEN}Damage Table{Style.RESET_ALL}
Shield Piercing: {dweapon['pierces_shields']}
Uses Missiles: {dweapon['uses_missiles']}

Hull Damage: {dweapon['hull_damage']}
Oxygen Taking: {dweapon['oxygen_damage']}
Power Usage: {dweapon['power_usage']}"""

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