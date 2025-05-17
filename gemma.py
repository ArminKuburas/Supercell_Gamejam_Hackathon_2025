from google import genai

client = genai.Client(api_key="AIzaSyAQDrrfmcduuqFB2EE_VCJU7ro57rs_ws8")
model_name = "gemma-3-27b-it"

# Initial setup of gameplay logic
game_state = {
	"npc_career": "Eastern Dragon",
	"npc_trait": "riddle speaking",
	"location": "dim moist sewers",
	"history": [
		"Eastern Dragon: One gives, one gains — yet which is which? The jewel finds a pocket, or the hand finds weight?",
		"Eastern Dragon: The path you seek bends like smoke. Follow the wind that does not blow.",
		"Eastern Dragon: A trembling leaf fears the breeze… yet is it not already falling?"
	]
}

# Initial player action
player_action = "Player: sneak"


# Prompt builder regenerated before passing new prompts
def build_prompt(game_state, player_action, history_length=6):
	npc_career = game_state["npc_career"]
	npc_trait = game_state["npc_trait"]
	location = game_state["location"]
	summary_history = " ".join(game_state["history"][-history_length:])

	prompt = f"""
You are **Gemma the Storyteller**, roleplaying a **{npc_trait} {npc_career}** in a dark medieval fantasy town. You are located in **{location}** and are interacting with a silent, blank-slate adventurer.

The world is bleak, twisted, and full of unreliable people. You must respond **in character**, using no more than 1–3 sentences.

You are allowed to respond to:
- Physical actions (e.g., offering an item, sitting, looking around)
- Basic emotional cues (e.g., fear, anger, sorrow, confusion)
- Short responses or gestures (e.g., nodding, saying “yes” or “no”)

Do not suggest options. Do not describe the adventurer. Do not explain. Just react naturally based on your personality and the current scene.

### Recent Scene History:
{summary_history}

### Adventurer’s Latest Input:
{player_action}

As the {npc_trait} {npc_career}, react now in 1–3 sentences.
""".strip()


	return prompt

# After each turn:
def update_history(game_state, player_input, npc_response):
	game_state["history"].append(f"Player: {player_input.strip().capitalize()}")
	game_state["history"].append(f"{game_state['npc_career']}: {npc_response}")


# Initial response

result = client.models.generate_content(
	model=model_name,
	contents=build_prompt(game_state, player_action)
)

print(f"{game_state['npc_career']}: ",result.text)
#game_state["history"].append(f"{game_state['npc_career']}: {result.text}")
update_history(game_state, player_action, result.text)


# Gameplay loop
while True:
	user_input = input("Player: ")
	if user_input.strip().lower() in ["exit", "quit"]:
		break

	player_action = "Player: " + user_input
	current_scene = build_prompt(game_state, player_action)
	result = client.models.generate_content(
	model=model_name,
	contents=current_scene
)
	print(f"{game_state['npc_career']}: ", result.text)
	update_history(game_state, player_action, result.text)
	#game_state["history"].append(f"{game_state['npc_career']}: {result.text}")
