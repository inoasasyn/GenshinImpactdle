import Character


def find_by_name(data, name):
    for x in data:
        if x.name.lower() == name.lower():
            return x
    return False


def find_by_element(data, element):
    for x in data:
        if x.element.lower() == element.lower():
            return True
    return False


def find_by_weapon_type(data, weapon_type):
    for x in data:
        if x.weapon_type.lower() == weapon_type.lower():
            return True
    return False


def find_by_region(data, region):
    for x in data:
        if x.region.lower() == region.lower():
            return True
    return False


def find_by_ascension_local_speciality(data, ascension_local_speciality):
    for x in data:
        if x.ascension_local_speciality.lower() == ascension_local_speciality.lower():
            return True
    return False


def find_by_ascension_boss_drop(data, ascension_boss_drop):
    for x in data:
        if x.ascension_boss_drop.lower() == ascension_boss_drop.lower():
            return True
    return False


def find_by_ascension_mob_drop(data, ascension_mob_drop):
    for x in data:
        if x.ascension_mob_drop.lower() == ascension_mob_drop.lower():
            return True
    return False
