def listify_dict(data, id_name='country_code'):
    '''
    go from a dict of dicts by id
    to an array with each dict and id added to the inner dicts
    '''
    items = []
    for k, item in data.items():
        item[id_name] = k
        items.append(item)
    return items

def dictify_list_of_dicts(data, key_name):
    '''
    input: a list of dicts each with at least one key of the name keyname
    output: a dict of dicts that includes the same dicts as the input
    keyed off of the values in those dicts referenced by key_name
    '''
    new_dict = {}
    for item in data:
        key = item[key_name]
        new_dict[key] = item
    return new_dict
