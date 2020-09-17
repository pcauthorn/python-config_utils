import unittest

from configutils.src import FileResolver


class TestFileResolver(unittest.TestCase):

    def test_yaml(self):
        f = FileResolver()
        a = f.get('configs/a.yaml')
        b = f.get('configs/b.yaml')
        self.assertNotEqual(a, b)
        self.assertIsInstance(a, dict)

    def test_json(self):
        f = FileResolver()
        a = f.get('configs/a.json')
        b = f.get('configs/b.json')
        self.assertNotEqual(a, b)
        self.assertIsInstance(a, dict)

    def test_provide_file_type(self):
        f = FileResolver(data_type='yaml')
        a = f.get('configs/a')
        self.assertIsInstance(a, dict)
        self.assertGreater(len(a), 0)


if __name__ == '__main__':
    unittest.main()
