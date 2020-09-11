import unittest
from copy import deepcopy

from configutils.code import update_dicts, UpdateConfig, ConfigKeys, ConfigDirectiveKeys


class TestUpdateDicts(unittest.TestCase):

    def test_simple(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        copy_o = deepcopy(o)
        copy_t = deepcopy(t)
        c = update_dicts(o, t)
        copy_o.update(copy_t)
        self.assertEqual(c, copy_o)

    def test_recursive(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        n1 = {5: 'e', 6: 'f', 'n': o}
        n2 = {5: 'f', 6: 'f', 'n': t}
        c = update_dicts(n1, n2)
        n1.update(n2)
        self.assertNotEqual(c, n1)

    def test_recursive_2(self):
        o = {1: 'a', 2: 'b'}
        t = {2: 'c', 4: 'd'}
        n1 = {5: 'e', 6: 'f', 'n': o}
        n2 = {5: 'f', 6: 'f', 'n': t}
        c = update_dicts(n1, n2)
        n2.pop('n')
        n1.update(n2)
        o.update(t)
        self.assertEqual(c, n1)


class TestUpdateConfig(unittest.TestCase):

    def test_simple(self):
        c = {ConfigKeys.Directive: {ConfigDirectiveKeys.Update: 'a'}, 1: 'a', 2: 'b'}
        update = {1: 'replaced1', 3: 'c'}
        resolver = {'a': update}
        updater = UpdateConfig(resolver=resolver)
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
        updater = UpdateConfig(resolver=resolver)
        updated = updater.update_config(c)
        result = deepcopy(c)
        result.update(update)
        result.update(update2)
        self.assertEqual(result, updated)
        self.assertNotEqual(c, updated)



if __name__ == '__main__':
    unittest.main()
