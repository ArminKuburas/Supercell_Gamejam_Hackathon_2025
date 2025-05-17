import json
import random
import os
import sys

def create_locations_json(csv_path, json_path):
    """
    Creates a JSON file from the CSV file.
    """
    import csv
    
    # Read the CSV file
    locations = []
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                locations.append(row["Location"])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        # Try reading as a simple CSV without headers
        try:
            locations = []
            with open(csv_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Skip empty rows
                        locations.append(row[0])
        except Exception as e:
            print(f"Error reading CSV without headers: {e}")
            return False
    
    # Create indexed locations
    indexed_locations = []
    for i, location in enumerate(locations):
        indexed_locations.append({
            "id": i,
            "name": location
        })
    
    # Create the final JSON structure
    json_data = {
        "locations": indexed_locations
    }
    
    # Write to JSON file
    try:
        with open(json_path, 'w') as file:
            json.dump(json_data, file, indent=4)  # Fixed order of arguments
        print(f"Successfully created {json_path}")
        return True
    except Exception as e:
        print(f"Error writing JSON: {e}")
        return False

def generate_random_character_and_location():
    """
    Randomly selects one class, one characteristic, and one location from the JSON files.
    
    Returns:
        dict: A dictionary containing the selected class, characteristic, and location
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to the JSON files
    character_json_path = os.path.join(script_dir, 'unrestricted_character_data.json')
    location_json_path = os.path.join(script_dir, 'indexed_locations.json')
    
    # Check if files exist
    if not os.path.exists(character_json_path):
        print(f"Error: Character data file not found at {character_json_path}")
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir(script_dir))
        sys.exit(1)
        
    if not os.path.exists(location_json_path):
        print(f"Error: Location data file not found at {location_json_path}")
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir(script_dir))
        
        # Try to find the locations.csv file and create the JSON
        csv_path = os.path.join(script_dir, 'city_locations.csv')
        if os.path.exists(csv_path):
            print(f"Found city_locations.csv, creating JSON file...")
            create_locations_json(csv_path, location_json_path)
        else:
            print(f"Could not find city_locations.csv either.")
            sys.exit(1)
    
    # Read the character JSON file
    with open(character_json_path, 'r') as file:
        character_data = json.load(file)
    
    # Read the location JSON file
    with open(location_json_path, 'r') as file:
        location_data = json.load(file)
    
    # Randomly select one class
    random_class = random.choice(character_data['classes'])
    
    # Randomly select one characteristic
    random_characteristic = random.choice(character_data['characteristics'])
    
    # Randomly select one location
    random_location = random.choice(location_data['locations'])
    
    # Create the result
    result = {
        "class": random_class,
        "characteristic": random_characteristic,
        "location": random_location
    }
    
    return result

def print_character_and_location(data):
    """
    Prints the character and location in a readable format.
    
    Args:
        data (dict): The data to print
    """
    print(f"Class: {data['class']['name']} (ID: {data['class']['id']})")
    print(f"Characteristic: {data['characteristic']['name']} (ID: {data['characteristic']['id']})")
    print(f"Location: {data['location']['name']} (ID: {data['location']['id']})")
    
    # Create a narrative sentence
    print(f"\nYou encounter a {data['characteristic']['name']} {data['class']['name']} at the {data['location']['name']}.")

if __name__ == "__main__":
    # Generate a character and location
    data = generate_random_character_and_location()
    print_character_and_location(data)
