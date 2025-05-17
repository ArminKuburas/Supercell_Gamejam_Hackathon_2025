import pygame
import os
import sys  # Import the sys module
from dialogue import DialogueCharacteristic

TRAIT_REACTIONS = {
    "shy": {
        "positive": {DialogueCharacteristic.COMPLIMENT, DialogueCharacteristic.PRAISE, DialogueCharacteristic.GREETING},
        "negative": {DialogueCharacteristic.INVITATION, DialogueCharacteristic.INSULT, DialogueCharacteristic.TEASE, DialogueCharacteristic.FLIRT}
    },
    "warrior": {
        "positive": {DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.POSITIVE, DialogueCharacteristic.ENCOURAGEMENT, DialogueCharacteristic.PRAISE, DialogueCharacteristic.REQUEST},
        "negative": {DialogueCharacteristic.INSULT, DialogueCharacteristic.NEGATIVE, DialogueCharacteristic.CRITICISM}
    },
    "intellectual": {
        "positive": {DialogueCharacteristic.MIND_COMMENT, DialogueCharacteristic.QUESTION, DialogueCharacteristic.PRAISE, DialogueCharacteristic.STATEMENT},
        "negative": {DialogueCharacteristic.INSULT, DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.TEASE}
    },
    "romantic": {
        "positive": {DialogueCharacteristic.FLIRT, DialogueCharacteristic.COMPLIMENT, DialogueCharacteristic.INVITATION, DialogueCharacteristic.PRAISE},
        "negative": {DialogueCharacteristic.INSULT, DialogueCharacteristic.CRITICISM, DialogueCharacteristic.TEASE}
    },
    "sarcastic": {
        "positive": {DialogueCharacteristic.JOKE, DialogueCharacteristic.TEASE, DialogueCharacteristic.CRITICISM},
        "negative": {DialogueCharacteristic.APOLOGY, DialogueCharacteristic.PRAISE, DialogueCharacteristic.FAREWELL}
    },
    "friendly": {
        "positive": {DialogueCharacteristic.GREETING, DialogueCharacteristic.PRAISE, DialogueCharacteristic.THANKS, DialogueCharacteristic.ENCOURAGEMENT},
        "negative": {DialogueCharacteristic.INSULT, DialogueCharacteristic.CRITICISM}
    },
    "serious": {
        "positive": {DialogueCharacteristic.STATEMENT, DialogueCharacteristic.REQUEST, DialogueCharacteristic.APOLOGY},
        "negative": {DialogueCharacteristic.JOKE, DialogueCharacteristic.TEASE, DialogueCharacteristic.FLIRT}
    },
    # Add more traits as needed...
}

TRAIT_PROMPTS = {
    "warrior": "You are a warrior, tough, confident, and focused on combat. You react positively to praise and encouragement, but negatively to weakness or criticism.",
    "shy": "You are shy, reserved, and easily embarrassed. You react positively to gentle compliments and kindness, but negatively to teasing or bold advances.",
    "intellectual": "You are an intellectual, curious and thoughtful. You appreciate deep questions and praise for your mind, but dislike shallow comments or insults.",
    "romantic": "You are romantic, affectionate, and enjoy flirtation. You react positively to compliments and invitations, but negatively to criticism or teasing.",
    "sarcastic": "You are sarcastic, witty, and often make jokes. You react positively to teasing and jokes, but negatively to praise or farewells.",
    "friendly": "You are friendly, warm, and supportive. You react positively to greetings, praise, and encouragement, but negatively to insults or criticism.",
    "serious": "You are serious, focused, and dislike jokes. You react positively to statements and requests, but negatively to jokes or flirtation.",
    # Add more as needed...
}

def get_asset_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Character:
    def __init__(self, name, character_name, char_type, personality_traits):
        self.base_dir = os.path.join("..", "assets", "characters")
        self.sprites = {
            "neutral": self.load_image(f"{character_name}_neutral"),
            "happy": self.load_image(f"{character_name}_happy"),
            "unhappy": self.load_image(f"{character_name}_unhappy"),
        }
        self.current_sprite = self.sprites["neutral"]
        self.name = name
        self.char_type = char_type
        self.personality_traits = personality_traits

    def load_image(self, character_name):
        image_path = get_asset_path(os.path.join(self.base_dir, f"{character_name}.png"))
        return pygame.image.load(image_path)

    def set_sprite_by_reaction(self, reaction):
        if reaction > 0:
            self.current_sprite = self.sprites["happy"]
        elif reaction < 0:
            self.current_sprite = self.sprites["unhappy"]
        else:
            self.current_sprite = self.sprites["neutral"]

    def react_to_dialogue(self, dialogue_option):
        reaction = 0
        for trait in self.personality_traits:
            trait_reactions = TRAIT_REACTIONS.get(trait, {})
            positives = trait_reactions.get("positive", set())
            negatives = trait_reactions.get("negative", set())
            # Check for positive matches
            if any(char in positives for char in dialogue_option.characteristics):
                reaction += 1
            # Check for negative matches
            if any(char in negatives for char in dialogue_option.characteristics):
                reaction -= 1
        return reaction
    def get_response_by_reaction(self, reaction):
        if reaction > 0:
            return "Thanks!"
        elif reaction < 0:
            return "Fuck you!"
        else:
            return "I feel neutral about this."

class Background:
    def __init__(self, background_name):
        self.base_dir = os.path.join("..", "assets", "backgrounds")
        self.name = background_name
        self.image = self.load_image(background_name)

    def load_image(self, background_name):
        image_path = get_asset_path(os.path.join(self.base_dir, f"{background_name}.png"))
        try:
            return pygame.image.load(image_path)
        except Exception:
            # Return a blank surface if not found
            surf = pygame.Surface((800, 300))  # Adjust size as needed
            surf.fill((255, 255, 255))
            return surf
    
PREDEFINED_CHARACTERS = [
    {
        "name": "John",
        "character_name": "john",
        "char_type": "warrior",
        "traits": ["warrior", "serious"],
        "backgrounds": ["alley", "shop", "townsquare", "jail", "sewers", "foodstalls"]
    },
    {
        "name": "Luna",
        "character_name": "luna",
        "char_type": "intellectual",
        "traits": ["intellectual", "shy"],
        "backgrounds": ["marketstreet", "sewers", "townsquare", "jail", "cursedwell", "shop"]
    },
    {
        "name": "Mika",
        "character_name": "mika",
        "char_type": "romantic",
        "traits": ["romantic", "friendly"],
        "backgrounds": ["shop", "sewers", "alley", "well", "cursedwell", "foodstalls"]
    },
    {
        "name": "Rex",
        "character_name": "rex",
        "char_type": "sarcastic",
        "traits": ["sarcastic", "serious"],
        "backgrounds": ["shop", "sewers", "alley", "well", "cursedwell", "foodstalls", "marketstreet"]
    },
    {
        "name": "Sophie",
        "character_name": "sophie",
        "char_type": "friendly",
        "traits": ["friendly", "shy"],
        "backgrounds": ["alley", "shop", "townsquare", "jail", "sewers", "foodstalls"]
    },
    # Add more as needed...
]
