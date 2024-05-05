import json


# Läser från json-fil och returnerar lista av innehåll
def read_from_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Creating a new file.")
        with open(file_path, "w") as file:
            json.dump([], file, indent=4)
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return []


# Skriver lista av innehåll till json-fil
def save_to_json_file(data, file_path):
    existing_data = read_from_json_file(file_path)

    for dict in data:
        existing_data.append(dict)

    try:
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data saved to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error saving data to '{file_path}': {e}")


def add_to_json(entitylist, new_entity, filename):
    entitylist.append(new_entity)
    save_to_json_file(entitylist, filename)



read_from_json_file("./main/static/timeblocks.json")