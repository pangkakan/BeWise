import json
import datetime


# Läser från json-fil och returnerar lista av innehåll
def read_from_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Creating a new file.")
        save_to_json_file([], file_path)
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return []


# Skriver lista av innehåll till json-fil
def save_to_json_file(data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error saving data to '{file_path}': {e}")


def add_to_json(entitylist, new_entity, filename):
    entitylist.append(new_entity)
    save_to_json_file(entitylist, filename)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)