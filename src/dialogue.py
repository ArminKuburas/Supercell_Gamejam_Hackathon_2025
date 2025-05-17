import pygame
from enum import Enum
import random

from config import FONT_SIZE

class DialogueCharacteristic(Enum):
    BODY_COMMENT = "body comments"
    MIND_COMMENT = "mind comments"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    INVITATION = "invitation"
    COMPLIMENT = "compliment"
    INSULT = "insult"
    QUESTION = "question"
    STATEMENT = "statement"
    ENCOURAGEMENT = "encouragement"
    JOKE = "joke"
    FLIRT = "flirt"
    APOLOGY = "apology"
    PRAISE = "praise"
    CRITICISM = "criticism"
    GREETING = "greeting"
    FAREWELL = "farewell"
    THANKS = "thanks"
    REQUEST = "request"
    TEASE = "tease"
    

class DialogueSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dialogue_options_list = dialogue_options  # Use the existing dialogue_options list
        self.selected_dialogue_options = self.select_random_dialogue_options()

    def select_random_dialogue_options(self):
        # Shuffle the list of dialogue options and select the first 4 unique options
        random.shuffle(self.dialogue_options_list)
        return self.dialogue_options_list[:4]

    def draw_dialogue_options(self, screen, font):
        box_height = 60
        gap = 10  # gap between boxes

    # Starting y-position for the bottom box (50 pixels from bottom)
        start_y = self.screen_height - box_height - 50  
        x = 50  # fixed x position for all boxes (left padding)

        for i, option in enumerate(self.selected_dialogue_options):
            y = start_y - i * (box_height + gap)
            text_width = font.size(option.text)[0]
            box_width = min(250, text_width + 40)  # max width 250
    
            option.rect = pygame.Rect(x, y, box_width, box_height)

            stone_gray = (120, 120, 120)
            border_light = (200, 200, 200)
            draw_stone_box(screen, option.rect, stone_gray, border_light, border_radius=12)
            draw_text(option.text, font, (255, 255, 255), screen, option.rect.centerx, option.rect.centery, max_width=box_width)

    def handle_click(self, pos):
        for option in self.selected_dialogue_options:
            if option.rect.collidepoint(pos):
                print(f"Selected: {option.text}")
                return option
        return None

def draw_stone_box(screen, rect, base_color, border_color, border_radius=10):
    # Draw shadow
    shadow_rect = rect.copy()
    shadow_rect.x += 4
    shadow_rect.y += 4
    shadow_color = (30, 30, 30, 100)  # semi-transparent dark
    shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=border_radius)
    screen.blit(shadow_surface, shadow_rect.topleft)

    # Draw main stone rectangle (solid fill)
    pygame.draw.rect(screen, base_color, rect, border_radius=border_radius)

    # Draw border outline (thickness 3)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=border_radius)

def draw_text(text, font, color, surface, x, y, max_width=None):
    # Adjust font size based on the length of the text and the max width of the box
    if max_width is not None:
        font_size = FONT_SIZE
        while font.size(text)[0] > max_width and font_size > 8:
            font_size -= 1
            font = pygame.font.SysFont(None, font_size)

    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


class DialogueOption:
    def __init__(self, text, characteristics):
        self.text = text
        self.characteristics = characteristics
        self.rect = pygame.Rect(0, 0, 200, 60)  # Default position and size

    def __repr__(self):
        return f"DialogueOption(text='{self.text}', characteristics={self.characteristics})"




dialogue_options = [
    DialogueOption("You have nice muscles!", [DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.POSITIVE, DialogueCharacteristic.COMPLIMENT]),
    DialogueOption("Let's go out sometime!", [DialogueCharacteristic.INVITATION, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You seem quite intelligent.", [DialogueCharacteristic.MIND_COMMENT, DialogueCharacteristic.POSITIVE, DialogueCharacteristic.COMPLIMENT]),
    DialogueOption("I don't like your attitude.", [DialogueCharacteristic.MIND_COMMENT, DialogueCharacteristic.NEGATIVE, DialogueCharacteristic.INSULT]),
    DialogueOption("How are you feeling today?", [DialogueCharacteristic.QUESTION, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You did a great job!", [DialogueCharacteristic.POSITIVE, DialogueCharacteristic.ENCOURAGEMENT]),
    DialogueOption("This is not good enough.", [DialogueCharacteristic.NEGATIVE, DialogueCharacteristic.INSULT]),
    DialogueOption("I think you can do better.", [DialogueCharacteristic.POSITIVE, DialogueCharacteristic.ENCOURAGEMENT]),
    DialogueOption("What do you think about this?", [DialogueCharacteristic.QUESTION, DialogueCharacteristic.STATEMENT]),
    DialogueOption("You look tired.", [DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("Hey there!", [DialogueCharacteristic.GREETING, DialogueCharacteristic.POSITIVE]),
    DialogueOption("Sorry about earlier.", [DialogueCharacteristic.APOLOGY, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("That was hilarious!", [DialogueCharacteristic.JOKE, DialogueCharacteristic.POSITIVE]),
    DialogueOption("Would you help me with this?", [DialogueCharacteristic.REQUEST, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You always know what to say.", [DialogueCharacteristic.PRAISE, DialogueCharacteristic.POSITIVE]),
    DialogueOption("Just kidding!", [DialogueCharacteristic.JOKE, DialogueCharacteristic.TEASE]),
    DialogueOption("You look amazing today.", [DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.COMPLIMENT, DialogueCharacteristic.POSITIVE]),
    DialogueOption("Goodbye for now.", [DialogueCharacteristic.FAREWELL, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("Thank you so much!", [DialogueCharacteristic.THANKS, DialogueCharacteristic.POSITIVE]),
    DialogueOption("That was a bit harsh.", [DialogueCharacteristic.CRITICISM, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("You make me laugh.", [DialogueCharacteristic.JOKE, DialogueCharacteristic.POSITIVE, DialogueCharacteristic.COMPLIMENT]),
    DialogueOption("Can I ask you something?", [DialogueCharacteristic.QUESTION, DialogueCharacteristic.REQUEST]),
    DialogueOption("You never listen!", [DialogueCharacteristic.CRITICISM, DialogueCharacteristic.NEGATIVE, DialogueCharacteristic.INSULT]),
    DialogueOption("Let's hang out soon.", [DialogueCharacteristic.INVITATION, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You handled that well.", [DialogueCharacteristic.PRAISE, DialogueCharacteristic.POSITIVE]),
    DialogueOption("That was uncalled for.", [DialogueCharacteristic.CRITICISM, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("I appreciate your help.", [DialogueCharacteristic.THANKS, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You always tease me!", [DialogueCharacteristic.TEASE, DialogueCharacteristic.NEGATIVE]),
    DialogueOption("I like your style.", [DialogueCharacteristic.COMPLIMENT, DialogueCharacteristic.BODY_COMMENT, DialogueCharacteristic.POSITIVE]),
    DialogueOption("You are so funny!", [DialogueCharacteristic.JOKE, DialogueCharacteristic.COMPLIMENT, DialogueCharacteristic.POSITIVE]),
]
