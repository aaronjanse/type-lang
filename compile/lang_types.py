type_name_translations = {
    'int': int,
    'str': str,
}


def is_type(value, type_name):
    if type_name == 'var':
        return True

    else:
        return isinstance(value, type_name_translations[type_name])
