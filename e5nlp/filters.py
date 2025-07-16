from pymorphy3 import MorphAnalyzer

ENTRIES_TO_EXCLUDE = [
    "другая",
    "без",
    "имени",
    "марка",
    "хуй",
    "пизда",
    "пидор",
    "господин",
    "повелитель",
    "хозяин",
    "нахуй",
    "соси",
    "царь",
    "пидераст",
]

morph: MorphAnalyzer | None = None

def _get_morph() -> MorphAnalyzer:
    global morph
    if not morph:
        morph = MorphAnalyzer()
    return morph


def filter_name(name: str | None) -> str | None:
    """
    Parse and filters first name
    """
    if not name:
        return None
    for entry in name.strip().lower().split(" "):
        if entry in ENTRIES_TO_EXCLUDE:
            continue
        parsed = _get_morph().parse(entry)
        if not parsed:
            continue
        if "Name" in parsed[0].tag.grammemes:
            return parsed[0].normal_form.capitalize()
    return None


def filter_full_name(name: str) -> str | None:
    """
    Filter full name
    """
    if not name:
        return None
    name = name.strip()
    first_name = ""
    surname = ""
    patronymic = ""
    for entry in name.split(" "):
        if entry in ENTRIES_TO_EXCLUDE:
            continue
        entries = _get_morph().parse(entry)
        grammemes = [p.tag.grammemes for p in entries][0]
        if "Name" in grammemes and "sing" in grammemes:
            first_name = entry.capitalize()
            continue
        if "Surn" in grammemes and "sing" in grammemes:
            patronymic = entry.capitalize()
            continue
        if "Patr" in grammemes and "sing" in grammemes:  # отчество
            surname = entry.capitalize()
            continue
    name = " ".join([first_name, surname, patronymic]).strip().replace("  ", " ")
    return name


def filter_text(text: str | None) -> str | None:
    """
    Filters arbitrary text
    """
    if not text:
        return None
    result = []
    for entry in text.strip().lower().split(" "):
        if entry in ENTRIES_TO_EXCLUDE:
            continue
        result.append(entry.capitalize())
    return " ".join(result) if result else None
