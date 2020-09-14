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
        updated = {1: '1u', 3: 'c'}
        resolver = {'a': updated}
        updater = ConfigUpdater(resolver=resolver)
        manual_update = updater.update_config(c)
        updated.update(c)
        self.assertEqual(manual_update, updated)

    def test_no_side_effects(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: 'a'}, 1: 'a', 2: 'b'}
        orig_config = deepcopy(c)
        updated = {1: '1u', 3: 'c'}
        resolver = {'a': updated}
        updater = ConfigUpdater(resolver=resolver)
        updated_config = updater.update_config(c)
        self.assertEqual(orig_config, c)
        self.assertNotEqual(orig_config, updated_config)

    def test_multiple(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: ['a', 'b']}, 1: 'a', 2: 'b'}
        update = {1: 'replaced1', 3: 'c'}
        update2 = {1: 'replaced2', 3: 'c2', 4: 'd'}
        resolver = {'a': update, 'b': update2}
        updater = ConfigUpdater(resolver=resolver)
        updated = updater.update_config(c)
        self.assertNotEqual(c, updated)
        self.assertEqual(updated[1], 'a')
        self.assertEqual(updated[4], 'd')
        self.assertEqual(updated[3], 'c2')

    def test_replace(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: 'a', ConfigDirectiveKeys.Replace: [4]},
             1: 'a',
             2: 'b',
             4: {2: 'just this'}}
        update = {1: 'replaced1', 3: 'c', 4: {'should be': 'all new'}}
        resolver = {'a': update}
        updater = ConfigUpdater(resolver=resolver)
        updated = updater.update_config(c)
        self.assertNotEqual(c, updated)
        self.assertDictEqual(updated[4], {2: 'just this'})

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

    def test_file_with_replace(self):
        resolver = FileResolver()
        updater = ConfigUpdater(resolver=resolver)
        with open('configs/config_replace.yaml', 'r') as f:
            config = load(f, Loader=Loader)
        result = updater.update_config(config)
        self.assertNotEqual(config, result)
        self.assertDictEqual(result['section']['config_part1'], config['section']['config_part1'])


if __name__ == '__main__':
    unittest.main()
