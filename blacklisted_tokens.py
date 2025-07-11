blacklist = set()


def add_to_blacklist(token: str):
    blacklist.add(token)


def is_blacklisted(token: str) -> bool:
    return token in blacklist
