from random import choice

def _fetch_kurisu_dialogue():
    with open("data/cleaned_amadeus_dialogue.csv", "r", encoding="utf-8") as dialogue_file:
        return dialogue_file.readlines()

def random_kurisu_line():
    KURISU_LINES = _fetch_kurisu_dialogue()
    return choice(KURISU_LINES)