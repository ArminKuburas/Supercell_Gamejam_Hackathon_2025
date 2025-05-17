import json

with open("gamestate.json", "r") as f:
    gamestate = json.load(f)

new_encounter = {
    "encounter_number": gamestate["encounter_count"] + 1,
    "location": "Underground Gambling Den",
    "npc_class": "Boastful Sellsword",
    "npc_traits": ["loud", "cocky"],
    "player_choice": "Confronted him about the priest",
    "result": "He challenged you to a duel at dawn"
}
