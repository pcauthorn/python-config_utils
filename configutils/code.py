from collections.abc import Mapping


class ConfigKeys:
    Directive = '__ConfigUtil_Directive'


class ConfigDirectiveKeys:
    Update = 'Update'
    Replace = 'Replace'


class ConfigUpdater:
    def __init__(self):
        pass


def update_dicts(base, the_update):
    if not isinstance(base, dict) or not isinstance(the_update, dict):
        raise TypeError(f'Both items should be dictionaries: {type(base)}, {type(the_update)}')
    for k, v in the_update.items():
        if isinstance(v, Mapping):
            i = base.get(k, {})
            if isinstance(i, Mapping):
                base[k] = update_dicts(i, v)
            else:
                base[k] = v
        else:
            base[k] = v
    return base


def update_config(c):
    pass


if __name__ == '__main__':
    print(update_dicts({'k1': 1}, {'k1': {'k2': {'k3': 3}}}))
