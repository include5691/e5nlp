import random

WELCOME_LIST = ["Здравствуйте", "Приветствую", "Доброго дня"]

def inject_marks(text: str, customer_name: str | None = None, car_name: str | None = None, user_name: str | None = None) -> str:
    """
    - {w} : welcome item
    - {n} : customer name
    - {c} : car name
    - {u} : user name
    """
    text = text.strip()
    if customer_name:
        if text[:3] != "{n}":
            customer_name = f", {customer_name}"
    else:
        customer_name = ""
    if car_name:
        car_name = f", {car_name}"
    else:
        car_name = ""
    if user_name:
        parts = user_name.split(" ")
        if len(parts) > 1:
            user_name = parts[1]
    else:
        user_name = ""
    if text[:2] == ", ":
        text = text[2:]
    welcome_item = random.choice(WELCOME_LIST)
    return text.format(w=welcome_item, n=customer_name, c=car_name, u=user_name).replace("  ", " ").replace(" ,", ",").replace(",,", ",").replace(", , ", ", ")