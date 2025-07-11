from re import search


def pwd_validator(value: str) -> str:
    if not search(r"[A-Z]", value):
        raise ValueError("The password must contain at least one capital letter.")
    if not search(r"[a-z]", value):
        raise ValueError("The password must contain at least one lowercase letter.")
    if not search(r"\d", value):
        raise ValueError("The password must contain at least one digit.")
    if not search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\\/\[\];']", value):
        raise ValueError("The password must contain at least one special symbol.")
    return value
