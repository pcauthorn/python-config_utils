import logging
from collections.abc import Mapping
from copy import deepcopy

logger = logging.getLogger(__name__)

UPDATES = {}


class ConfigKeys:
    Directive = '__ConfigUtil_Directive'


class ConfigDirectiveKeys:
    Update = 'Update'
    Replace = 'Replace'


class ConfigUpdater:
    def __init__(self):
        pass


def update_dicts(base, the_update, replace=None):
    if not isinstance(base, dict) or not isinstance(the_update, dict):
        raise TypeError(f'Both items should be dictionaries: {type(base)}, {type(the_update)}')
    base = deepcopy(base)
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


class UpdateConfig:
    def __init__(self, resolver=None):
        self.resolver = resolver  # write a file resolver, default to this if resolver is None

    def update_config(self, c):
        if ConfigKeys.Directive not in c:
            logger.warning(f'No Directive Key ({ConfigKeys.Directive}), not doing anything')
            return deepcopy(c)
        result = deepcopy(c)
        directive = c[ConfigKeys.Directive]
        updates = directive.get(ConfigDirectiveKeys.Update)
        if not isinstance(updates, list):
            updates = [updates]
        for update in updates:
            i = self.resolver.get(update)
            if not i:
                logger.warning(f'Could not find update: {update} with resolver {self.resolver}, skipping')
                continue
            result = update_dicts(result, i)
        return result


if __name__ == '__main__':
    print(update_dicts({'k1': 1}, {'k1': {'k2': {'k3': 3}}}))
