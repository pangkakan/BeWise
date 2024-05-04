# Generell funktion som tar emot listor av lexikon där man utgår från att alla lexikon har id-nyckel
def create_id(list_of_dictionaries):
    highest_id = 1
    for dictionary in list_of_dictionaries:
        if dictionary["id"] >= highest_id:
            highest_id = dictionary["id"] + 1
    return highest_id
