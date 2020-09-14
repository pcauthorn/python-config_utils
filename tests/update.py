import unittest
from copy import deepcopy
from yaml import Loader, load

from configutils.code import update_dicts, ConfigUpdater, ConfigKeys, ConfigDirectiveKeys, FileResolver


class TestUpdateDicts(unittest.TestCase):

    def test_simple(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        copy_o = deepcopy(o)
        copy_t = deepcopy(t)
        c = update_dicts(o, t)
        copy_o.update(copy_t)
        self.assertEqual(c, copy_o)

    def test_recursive_negative_case(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        n1 = {5: 'e', 6: 'f', 'n': o}
        n2 = {5: 'f', 6: 'f', 'n': t}
        c = update_dicts(n1, n2)
        n1.update(n2)
        self.assertNotEqual(c, n1)

    def test_recursive(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        n1 = {5: 'e', 6: 'f', 'n': o}
        n2 = {5: 'f', 6: 'f', 'n': t}
        c = update_dicts(n1, n2)
        n2.pop('n')
        n1.update(n2)
        o.update(t)
        self.assertEqual(c, n1)

    def test_replace(self):
        o = {1: 'should be gone', 2: 'this too'}
        t = {2: 'stay', 4: 'stay'}
        n1 = {4: 'gone', 6: 'f', 'n': o}
        n2 = {5: 'f', 6: 'f', 'n': t}
        c = update_dicts(n1, n2, replace=['n'])
        self.assertEqual(set(c['n'].values()), {'stay'})
        n1.update(n2)
        self.assertEqual(c, n1)

    def test_replace_nested(self):
        n1 = {4: 'e', 6: 'f', 'n': {1: {2: {'a': 'should be gone'}}}}
        n2 = {5: 'f', 6: 'f', 'n': {1: {2: {'c': 'stay'}}}}
        c = update_dicts(n1, n2, replace=['n', 1, 2])
        self.assertEqual(c['n'][1][2], {'c': 'stay'})
        d = update_dicts(n1, n2)
        self.assertNotEqual(d['n'][1][2], {'c': 'stay'})


class TestConfigUpdater(unittest.TestCase):

    def test_simple(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: 'a'}, 1: 'a', 2: 'b'}
        update = {1: 'replaced1', 3: 'c'}
        resolver = {'a': update}
        updater = ConfigUpdater(resolver=resolver)
        updated = updater.update_config(c)
        result = deepcopy(c)
        result.update(update)
        self.assertEqual(result, updated)
        self.assertNotEqual(c, updated)

    def test_multiple(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: ['a', 'b']}, 1: 'a', 2: 'b'}
        update = {1: 'replaced1', 3: 'c'}
        update2 = {1: 'replaced2', 4: 'c'}
        resolver = {'a': update, 'b': update2}
        updater = ConfigUpdater(resolver=resolver)
        updated = updater.update_config(c)
        result = deepcopy(c)
        result.update(update)
        result.update(update2)
        self.assertEqual(result, updated)
        self.assertNotEqual(c, updated)

    def test_replace(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: 'a', ConfigDirectiveKeys.Replace: [4]},
             1: 'a',
             2: 'b',
             4: {2: 'should be gone', 1: 'should be gone'}}
        update = {1: 'replaced1', 3: 'c', 4: {'should be': 'all new'}}
        resolver = {'a': update}
        updater = ConfigUpdater(resolver=resolver)
        updated = updater.update_config(c)
        result = deepcopy(c)
        result.update(update)
        self.assertEqual(result, updated)
        self.assertNotEqual(c, updated)

    def test_with_resolver(self):
        resolver = FileResolver()
        updater = ConfigUpdater(resolver=resolver)
        with open('configs/config.yaml', 'r') as f:
            config = load(f, Loader=Loader)
        result = updater.update_config(config)
        self.assertNotEqual(config, result)
        with open('configs/a.yaml', 'r') as f:
            a = load(f, Loader=Loader)
        config['section'].update(a['section'])
        self.assertEqual(config, result)


if __name__ == '__main__':
    unittest.main()
