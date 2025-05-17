import pygame
import sys
from dialogue import DialogueSystem, DialogueOption, DialogueCharacteristic
from characters import Character, Background
from config import FONT_SIZE

import random
from characters import PREDEFINED_CHARACTERS

# Initialize Pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visual Novel")

# Set up fonts
font = pygame.font.SysFont(None, FONT_SIZE)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def fade_to_black(surface, duration=1000):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 25)

def pick_new_character(exclude_index=None):
    indices = list(range(len(PREDEFINED_CHARACTERS)))
    if exclude_index is not None:
        indices.remove(exclude_index)
    idx = random.choice(indices)
    char_info = PREDEFINED_CHARACTERS[idx]
    bg_name = random.choice(char_info["backgrounds"])
    character = Character(char_info["name"], char_info["character_name"], char_info["char_type"], char_info["traits"])
    background = Background(bg_name)
    return character, background, idx

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)
        pygame.draw.rect(screen, BLACK, button_1)
        pygame.draw.rect(screen, BLACK, button_2)
        pygame.draw.rect(screen, BLACK, button_3)
        draw_text("Play", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text("Options", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        draw_text("Quit", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint((mx, my)):
                    game_loop()  # Start the game
                if button_2.collidepoint((mx, my)):
                    options_menu()  # Open options menu
                if button_3.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options_menu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen  # Declare screen as global
    while True:
        screen.fill(BLACK)
        draw_text('Options Menu', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)
        pygame.draw.rect(screen, BLACK, button_1)
        pygame.draw.rect(screen, BLACK, button_2)
        pygame.draw.rect(screen, BLACK, button_3)
        draw_text("800x600", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text("1024x768", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        draw_text("Back", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint((mx, my)):
                    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                if button_2.collidepoint((mx, my)):
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                if button_3.collidepoint((mx, my)):
                    return  # Return to main menu

        pygame.display.update()

# ...existing code...

def draw_speech_bubble(text, font, color, surface, center_x, bottom_y, bubble_width=500, bubble_height=80, bubble_color=(255, 255, 255), border_color=(0, 0, 0), border_width=3):
    # Bubble rectangle (rounded)
    bubble_rect = pygame.Rect(center_x - bubble_width // 2, bottom_y - bubble_height, bubble_width, bubble_height)
    
    # Draw bubble background with border
    pygame.draw.rect(surface, border_color, bubble_rect, border_radius=20)   # border
    pygame.draw.rect(surface, bubble_color, bubble_rect.inflate(-border_width*2, -border_width*2), border_radius=20)  # inner bubble
    
    # Draw the tail as a triangle pointing downwards (you can adjust position)
    wrapped_lines = []
    words = text.split(' ')
    line = ""
    padding = 15
    max_text_width = bubble_width - padding * 2
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] > max_text_width:
            wrapped_lines.append(line)
            line = word + " "
        else:
            line = test_line
    wrapped_lines.append(line)
    
    # Draw each line centered inside the bubble with padding
    for i, line in enumerate(wrapped_lines):
        line_surf = font.render(line.strip(), True, color)
        line_rect = line_surf.get_rect(center=(center_x, bubble_rect.top + padding + i * font.get_linesize()))
        surface.blit(line_surf, line_rect)

def draw_dialogue_box(text, font, color, surface, center_x, bottom_y, box_width=500, box_height=80, box_color=(0,0,0)):
    # Draw the box
    box_rect = pygame.Rect(center_x - box_width // 2, bottom_y - box_height, box_width, box_height)
    pygame.draw.rect(surface, box_color, box_rect, border_radius=12)
    # Fit text inside the box
    wrapped_lines = []
    words = text.split(' ')
    line = ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] > box_width - 20:
            wrapped_lines.append(line)
            line = word + " "
        else:
            line = test_line
    wrapped_lines.append(line)
    # Draw each line centered
    for i, line in enumerate(wrapped_lines):
        line_surf = font.render(line.strip(), True, color)
        line_rect = line_surf.get_rect(center=(center_x, box_rect.top + 20 + i * font.get_height()))
        surface.blit(line_surf, line_rect)

def game_loop():
    current_idx = random.randint(0, len(PREDEFINED_CHARACTERS) - 1)
    char_info = PREDEFINED_CHARACTERS[current_idx]
    character = Character(char_info["name"], char_info["character_name"], char_info["char_type"], char_info["traits"])
    background = Background(random.choice(char_info["backgrounds"]))
    dialogue_system = DialogueSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    last_response = ""
    conversations = 0

    while True:
        screen.fill(BLACK)
        scaled_background = pygame.transform.scale(background.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_background, (0, 0))

        char_width, char_height = character.current_sprite.get_size()
        aspect_ratio = char_width / char_height
        new_char_height = SCREEN_HEIGHT - 50
        new_char_width = int(new_char_height * aspect_ratio)
        scaled_character = pygame.transform.smoothscale(character.current_sprite, (new_char_width, new_char_height))
        offset_x = 250
        offset_y = 100
        screen.blit(scaled_character, (SCREEN_WIDTH // 2 - new_char_width // 2 + offset_x, SCREEN_HEIGHT // 4 - offset_y))

        dialogue_system.draw_dialogue_options(screen, font)

        # Draw the character's response above the character
        if last_response:
            char_box_center_x = SCREEN_WIDTH // 2
            char_box_bottom_y = SCREEN_HEIGHT // 4
            draw_speech_bubble(
                last_response,
                font,
                (0, 0, 0),
                screen,
                char_box_center_x - 90,
                char_box_bottom_y - 50,
                bubble_width=500,
                bubble_height=80,
                bubble_color=(255, 255, 255),
                border_color=(0, 0, 0),
                border_width=3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if conversations < 5:
                    selected_option = dialogue_system.handle_click(event.pos)
                    if selected_option:
                        reaction = character.react_to_dialogue(selected_option)
                        character.set_sprite_by_reaction(reaction)
                        last_response = character.get_response_by_reaction(reaction)
                        dialogue_system.selected_dialogue_options = dialogue_system.select_random_dialogue_options()
                        conversations += 1

        # If 5 conversations reached, show prompt and wait for SPACE
        if conversations >= 5:
            waiting_for_space = True
            while waiting_for_space:
                # Draw everything as usual
                screen.fill(BLACK)
                scaled_background = pygame.transform.scale(background.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(scaled_background, (0, 0))

                char_width, char_height = character.current_sprite.get_size()
                aspect_ratio = char_width / char_height
                new_char_height = SCREEN_HEIGHT - 50
                new_char_width = int(new_char_height * aspect_ratio)
                scaled_character = pygame.transform.smoothscale(character.current_sprite, (new_char_width, new_char_height))
                offset_x = 250
                offset_y = 100
                screen.blit(scaled_character, (SCREEN_WIDTH // 2 - new_char_width // 2 + offset_x, SCREEN_HEIGHT // 4 - offset_y))

                dialogue_system.draw_dialogue_options(screen, font)

                # Draw the character's response above the character
                if last_response:
                    char_box_center_x = SCREEN_WIDTH // 2
                    char_box_bottom_y = SCREEN_HEIGHT // 4
                    draw_speech_bubble(
                        last_response,
                        font,
                        (0, 0, 0),
                        screen,
                        char_box_center_x - 90,
                        char_box_bottom_y - 50,
                        bubble_width=500,
                        bubble_height=80,
                        bubble_color=(255, 255, 255),
                        border_color=(0, 0, 0),
                        border_width=3)

                # Draw the "Press SPACE" prompt
                draw_speech_bubble(
                    "Press SPACE to meet the next character!",
                    font,
                    (0, 0, 0),
                    screen,
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    bubble_width=500,
                    bubble_height=80,
                    bubble_color=(255, 255, 255),
                    border_color=(0, 0, 0),
                    border_width=3)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return
                        if event.key == pygame.K_SPACE:
                            waiting_for_space = False

            # After exiting the loop, fade and switch character
            fade_to_black(screen)
            character, background, current_idx = pick_new_character(exclude_index=current_idx)
            dialogue_system.selected_dialogue_options = dialogue_system.select_random_dialogue_options()
            last_response = ""
            conversations = 0
        
if __name__ == "__main__":
    main_menu()

