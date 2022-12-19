import toml

databank = {
    "species": toml.load("databank/species.toml"),
    "weapon": toml.load("databank/weapons.toml"),
    "creature": toml.load("databank/creatures.toml"),
    "disease": toml.load("databank/diseases.toml"),
    "faction": toml.load("databank/factions.toml"),
    "sector": toml.load("databank/sectors.toml"),
}

def get_item_databank(db: str, item: str):
    return databank[db][item]