from colorama import Fore, Back, Style
from databank import databank, get_item_databank
import re

def character(character_dict: dict) -> str:
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
    return message

def species(species: str):
    message = f"species not found, {species}"
    if species in databank["species"]:
        message = f"""{Style.BRIGHT}{Fore.RED}{databank["species"][species]['plural']} ({databank["species"][species]['single']}){Style.RESET_ALL}
        {databank["species"][species]['description']}"""

    return message

def faction(faction_string: str):
    message = f"faction not found, {faction_string}"

    if faction_string in databank["faction"]:
        faction = get_item_databank("faction", faction_string)

        enemies = faction["enemies"].split(",")
        allies = faction["allies"].split(",")

        def pretty(array):
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

    return message

def weapon(weapon: str):
    message = f"weapon not found, {weapon}"
    if weapon in databank["weapon"]:
        dweapon = get_item_databank("weapon", weapon)
        message = f"""{Style.BRIGHT}{Fore.GREEN}{dweapon['name']}{Style.RESET_ALL}
    {dweapon['description']}

    Shield Piercing: {dweapon['pierces_shields']}
    Uses Missiles: {dweapon['uses_missiles']}

{Style.BRIGHT}{Fore.GREEN}Damage Table{Style.RESET_ALL}
    Hull Damage: {dweapon['hull_damage']}
    Oxygen Taking: {dweapon['oxygen_damage']}
    Power Usage: {dweapon['power_usage']}"""

    return message

def anti_ansi(string: str) -> str:
    """Removes all ANSI escape sequences from a string."""

    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', string)