from json_manager import save_to_json_file


def add_timeblock(timeblocks, timeblock_data):
    timeblocks.append(timeblock_data)
    save_to_json_file(timeblocks, "static/timeblocks.json")
