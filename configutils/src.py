import json
import logging
import re
from collections.abc import Mapping
from copy import deepcopy

import yaml
from yaml import Loader

logger = logging.getLogger(__name__)


class ConfigKeys:
    Directive = '__ConfigUtil_Directive'


class ConfigDirectiveKeys:
    Update = 'Update'
    Replace = 'Replace'


def _get_nested_replace(k, replace):
    """
    replace is looks like this:
    ['k1', 'k2', 'k3', ['k4', 'k1']]
    strings are keys in the current dict, list would be for keys in a nested dict.
    Note: any key that is a string wouldn't also be the first element in a list
    This is because the string keys whole dict will get replaced
    """
    return [a[1] if len(a) == 2 else a[1:] for a in replace if isinstance(a, list) and a and a[0] == k]


def update_dicts(base, the_update, replace=None):
    if not isinstance(base, dict) or not isinstance(the_update, dict):
        raise TypeError(f'Both items should be dictionaries: {type(base)}, {type(the_update)}')
    replace = replace or []
    base = deepcopy(base)
    for k, v in the_update.items():
        if isinstance(v, Mapping) and k not in replace:
            i = base.get(k, {})
            if isinstance(i, Mapping):
                base[k] = update_dicts(i, v, replace=_get_nested_replace(k, replace))
            else:
                base[k] = v
        else:
            base[k] = v
    return base


class FileResolver:
    def __init__(self, data_type=None):
        self.data_type = data_type

    def get(self, file_name):
        if not self.data_type:
            data_type = re.split(r'[/\\]', file_name)[-1]
            data_type = data_type.split('.')
            if len(data_type) == 2:
                data_type = data_type[1]
            else:
                logger.warning(f'Could not determine datatype with file {file_name}, using json')
                data_type = 'json'
        else:
            data_type = self.data_type
        with open(file_name, 'r') as f:
            if data_type == 'yaml':
                result = yaml.load(f, Loader=Loader)
            elif data_type == 'json':
                result = json.load(f)
            else:
                raise TypeError(f'No support for file type {data_type}')
        return result


class ConfigUpdater:
    def __init__(self, resolver=None):
        self.resolver = resolver or FileResolver()

    def update_config(self, c):
        if ConfigKeys.Directive not in c:
            logger.warning(f'No Directive Key ({ConfigKeys.Directive}), not doing anything')
            return deepcopy(c)
        directive = c[ConfigKeys.Directive]
        updates = directive.get(ConfigDirectiveKeys.Update)
        replace = directive.get(ConfigDirectiveKeys.Replace)
        if not isinstance(updates, list):
            updates = [updates]
        result = {}
        for update in updates:
            i = self.resolver.get(update)
            if not i:
                logger.warning(f'Could not find update: {update} with resolver {self.resolver}, skipping')
                continue
            result = update_dicts(result, i, replace=replace)
        result = update_dicts(result, c, replace=replace)
        return result
