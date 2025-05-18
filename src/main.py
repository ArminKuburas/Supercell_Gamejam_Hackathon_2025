import pygame
import sys
from dialogue import DialogueSystem, DialogueOption, DialogueCharacteristic
from characters import Character, Background, TRAIT_PROMPTS, TRAIT_REACTIONS
from config import FONT_SIZE
import getpass
from google import genai
import csv

import random
from characters import PREDEFINED_CHARACTERS

# Initialize Pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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

def load_logo_image():
    """Helper function to load the logo image"""
    try:
        # Try the exact path specified
        logo_path = 'assets/backgrounds/logo.jpeg'
        print(f"Attempting to load logo from: {logo_path}")
        logo_image = pygame.image.load(logo_path)
        print(f"Successfully loaded logo from: {logo_path}")
        return logo_image
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading from primary path: {e}")
        
        # Try alternative paths as fallback
        alternative_paths = [
            'assets/backgrounds/logo.jpg',
            '../assets/backgrounds/logo.jpeg',
            '../assets/backgrounds/logo.jpg',
            'assets/logo.jpeg',
            'assets/logo.jpg'
        ]
        
        for path in alternative_paths:
            try:
                print(f"Attempting to load logo from: {path}")
                logo_image = pygame.image.load(path)
                print(f"Successfully loaded logo from: {path}")
                return logo_image
            except (pygame.error, FileNotFoundError) as e:
                print(f"Failed to load from {path}: {e}")
                
        print("WARNING: Could not load logo image from any path. Using black background instead.")
        return None

def main_menu():
    # Load the logo image
    logo_image = load_logo_image()
    
    # Create a semi-transparent overlay for better text visibility
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    
    while True:
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the logo if available
        if logo_image:
            # Scale the logo to fit the screen
            scaled_logo = pygame.transform.scale(logo_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_logo, (0, 0))
            
            # Add semi-transparent overlay for better text visibility
            screen.blit(overlay, (0, 0))
        else:
            # If logo couldn't be loaded, just use black background
            screen.fill(BLACK)
        
        # Draw the title
        title_font = pygame.font.SysFont(None, FONT_SIZE * 2)  # Larger font for title
        # draw_text('Visual Novel', title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()

        # Create button rectangles
        button_width = 200
        button_height = 50
        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 20, button_width, button_height)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 90, button_width, button_height)
        
        # Draw buttons with hover effect
        for button, text, y_pos in [
            (button_1, "Play", SCREEN_HEIGHT // 2 - 25),
            (button_2, "Options", SCREEN_HEIGHT // 2 + 45),
            (button_3, "Quit", SCREEN_HEIGHT // 2 + 115)
        ]:
            # Check if mouse is over button
            if button.collidepoint((mx, my)):
                button_color = (100, 100, 100)  # Lighter when hovered
            else:
                button_color = (50, 50, 50)  # Darker when not hovered
                
            # Draw button with border
            pygame.draw.rect(screen, WHITE, button, border_radius=10)  # Border
            pygame.draw.rect(screen, button_color, button.inflate(-4, -4), border_radius=8)  # Button
            draw_text(text, font, WHITE, screen, button.centerx, button.centery)

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

def build_ai_prompt(character, background, conversation_history, player_message):
    # Get trait description
    trait_desc = " ".join([TRAIT_PROMPTS.get(trait, "") for trait in character.personality_traits])
    env_desc = f"The environment is {background}."
    # Format conversation history
    history_lines = []
    for entry in conversation_history:
        history_lines.append(f"Player: {entry['player']}")
        history_lines.append(f"NPC: {entry['npc']}")
    history_text = " ".join(history_lines)
    # Build prompt
    prompt = (
        f"{trait_desc} {env_desc} Previous interactions: {history_text} "
        f"Player's message: {player_message} "
        "The NPC should respond in character, in 1-2 sentences, with the appropriate tone. Please make sure that each sentence is very short. Please make sure to incorporate information from previous interactions. Do not use any emojis just regular words and keep it simple. no blushing, warm face, etc."
    )
    return prompt

def get_npc_response(client, model_name, prompt):
    response = client.models.generate_content(
        model=model_name,
        contents=[prompt]
    )
    print(f"AI Response: {response.text.strip()}")
    return response.text.strip()

def prompt_for_api_key():
    print("Please enter your Gemini API key (input hidden):")
    return getpass.getpass("API Key: ")

# Prompt for API key and initialize Gemini client
api_key = prompt_for_api_key()
client = genai.Client(api_key=api_key)
model_name = "gemma-3-27b-it"

def restart_game(new_width, new_height):
    """Completely restart the game with new resolution settings"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, font
    
    # Update the global variables
    SCREEN_WIDTH = new_width
    SCREEN_HEIGHT = new_height
    
    # Quit pygame completely
    pygame.quit()
    
    # Restart pygame from scratch
    pygame.init()
    
    # Set up the display with new dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Visual Novel")
    
    # Reinitialize font
    font = pygame.font.SysFont(None, FONT_SIZE)
    
    # Start the game from the main menu
    main_menu()

def options_menu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    
    # Store original dimensions
    original_width, original_height = SCREEN_WIDTH, SCREEN_HEIGHT
    
    # Load the logo image
    logo_image = load_logo_image()
    
    # Create overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    
    while True:
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the logo if available
        if logo_image:
            scaled_logo = pygame.transform.scale(logo_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_logo, (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            # If logo couldn't be loaded, just use black background
            screen.fill(BLACK)
        
        # Draw the title
        draw_text('Options Menu', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        mx, my = pygame.mouse.get_pos()

        # Create button rectangles
        button_width = 200
        button_height = 50
        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 20, button_width, button_height)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 90, button_width, button_height)
        button_4 = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 160, button_width, button_height)
        
        # Draw buttons with hover effect
        for button, text, y_pos in [
            (button_1, "800x600", SCREEN_HEIGHT // 2 - 25),
            (button_2, "1024x768", SCREEN_HEIGHT // 2 + 45),
            (button_3, "1920x1080", SCREEN_HEIGHT // 2 + 115),
            (button_4, "Back to Menu", SCREEN_HEIGHT // 2 + 185)
        ]:
            # Check if mouse is over button
            if button.collidepoint((mx, my)):
                button_color = (100, 100, 100)  # Lighter when hovered
            else:
                button_color = (50, 50, 50)  # Darker when not hovered

            # Draw button with border
            pygame.draw.rect(screen, WHITE, button, border_radius=10)  # Border
            pygame.draw.rect(screen, button_color, button.inflate(-4, -4), border_radius=8)  # Button
            draw_text(text, font, WHITE, screen, button.centerx, button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint((mx, my)):
                    if SCREEN_WIDTH != 800 or SCREEN_HEIGHT != 600:
                        restart_game(800, 600)
                        return  # This return is important as we've restarted the game
                
                if button_2.collidepoint((mx, my)):
                    if SCREEN_WIDTH != 1024 or SCREEN_HEIGHT != 768:
                        restart_game(1024, 768)
                        return  # This return is important as we've restarted the game
                
                if button_3.collidepoint((mx, my)):
                    restart_game(1920, 1080)
                    return  # This return is important as we've restarted the game
                if button_4.collidepoint((mx, my)):
                    # Go back to main menu
                    return
        pygame.display.update()

def draw_speech_bubble(text, font, color, surface, center_x, bottom_y, bubble_width=500, bubble_height=150, bubble_color=(255, 255, 255), border_color=(0, 0, 0), border_width=3):
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

def load_backgrounds_from_csv(csv_path):
    backgrounds = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            backgrounds.append({
                "name": row["background_name"],
                "display": row.get("display_name", row["background_name"])
            })
    return backgrounds

ALL_BACKGROUNDS = load_backgrounds_from_csv("../assets/characteristics/city_locations.csv")

def choose_next_location():
    # Pick 4 random backgrounds
    options = random.sample(ALL_BACKGROUNDS, 4)
    while True:
        screen.fill(WHITE)
        draw_text("Choose your next location:", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        buttons = []
        for i, bg in enumerate(options):
            btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + i * 70, 300, 50)
            pygame.draw.rect(screen, BLACK, btn_rect)
            draw_text(bg["display"], font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 70 + 25)
            buttons.append((btn_rect, bg["name"]))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for btn_rect, bg_name in buttons:
                    if btn_rect.collidepoint((mx, my)):
                        return bg_name

def game_loop():
    current_idx = random.randint(0, len(PREDEFINED_CHARACTERS) - 1)
    char_info = PREDEFINED_CHARACTERS[current_idx]
    character = Character(char_info["name"], char_info["character_name"], char_info["char_type"], char_info["traits"])
    background = Background(random.choice(char_info["backgrounds"]))
    dialogue_system = DialogueSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    last_response = ""
    conversations = 0
    conversation_history = []

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
                char_box_bottom_y + 30,
                bubble_width=500,
                bubble_height=200,
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
                        player_message = selected_option.text
                        print(f"Player selected: {player_message}")
                        # Build AI prompt
                        background_name = background.name
                        ai_prompt = build_ai_prompt(character, background_name, conversation_history, player_message)
                        print(f"AI Prompt: {ai_prompt}")
                        # Get AI response
                        npc_response = get_npc_response(client, model_name, ai_prompt)
                        # Save to history
                        conversation_history.append({"player": player_message, "npc": npc_response})
                        # Update visuals
                        reaction = character.react_to_dialogue(selected_option)
                        character.set_sprite_by_reaction(reaction)
                        last_response = npc_response
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
                if last_response:
                    char_box_center_x = SCREEN_WIDTH // 2
                    char_box_bottom_y = SCREEN_HEIGHT // 4
                    draw_speech_bubble(
                        last_response,
                        font,
                        (0, 0, 0),
                        screen,
                        char_box_center_x - 90,
                        char_box_bottom_y + 30,
                        bubble_width=500,
                        bubble_height=200,
                        bubble_color=(255, 255, 255),
                        border_color=(0, 0, 0),
                        border_width=3)
                draw_speech_bubble(
                    "Press SPACE to choose your next location!",
                    font,
                    (0, 0, 0),
                    screen,
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    bubble_width=500,
                    bubble_height=200,
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

            # 2. Let player choose next location
            next_bg_name = choose_next_location()
            background = Background(next_bg_name)

            # After exiting the loop, fade and switch character
            fade_to_black(screen)
            character, background, current_idx = pick_new_character(exclude_index=current_idx)
            dialogue_system.selected_dialogue_options = dialogue_system.select_random_dialogue_options()
            last_response = ""
            conversations = 0
            conversation_history = []

if __name__ == "__main__":
    main_menu()

