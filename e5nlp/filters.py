from pymorphy3 import MorphAnalyzer

ENTRIES_TO_EXCLUDE = ["другая", "без", "имени", "марка", "хуй", "пизда", "пидор", "господин", "повелитель", "хозяин", "нахуй", "соси", "царь", "пидераст"]

morph: MorphAnalyzer | None = None

def filter_name(name: str | None) -> str | None:
    """
    Parse and filters first name
    """
    global morph
    if not morph:
        morph = MorphAnalyzer()
    for entry in name.strip().lower().split(" "):
        if entry in ENTRIES_TO_EXCLUDE:
            continue
        parsed = morph.parse(entry)
        if not parsed:
            continue
        if "Name" in parsed[0].tag.grammemes:
            return parsed[0].normal_form.capitalize()
    return None

def filter_text(text: str | None) -> str | None:
    """
    Filters arbitrary text
    """
    result = []
    for entry in text.strip().lower().split(" "):
        if entry in ENTRIES_TO_EXCLUDE:
            continue
        result.append(entry.capitalize())
    return " ".join(result) if result else None