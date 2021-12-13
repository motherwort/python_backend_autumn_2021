import unittest
from levenshtein import get_levenshtein_distance as ld


class TestLevenshteinDistance(unittest.TestCase):
    def assert_ld(self, a, b, result):
        self.assertEqual(ld(a, b), result)
        self.assertEqual(ld(b, a), result)

    def test_two_empty_strings(self):
        self.assert_ld('', '', 0)

    def test_one_empty_strings(self):
        self.assert_ld('', 'дом', 3)
        self.assert_ld('', 'дорога', 6)

    def test_lowercase_uppercase(self):
        self.assert_ld('cтрока', 'СТРОКА', 6)
        self.assert_ld('собака', 'СОБАКА', 6)
        self.assert_ld('дом', 'ДОМ', 3)    

    def test_equal_words(self):
        self.assert_ld('cтрока', 'cтрока', 0)
        self.assert_ld('собака', 'собака', 0)
        self.assert_ld('СОБАКА', 'СОБАКА', 0)
        self.assert_ld('дорога', 'дорога', 0)
        self.assert_ld('перегрузить', 'перегрузить', 0)

    def test_different_words(self):
        self.assert_ld('cтрока', 'собака', 4)
        self.assert_ld('природный', 'бездомник', 7)
        self.assert_ld('богомильство', 'преграждение', 12)
        self.assert_ld('перегрузить', 'перестройка', 7)
        self.assert_ld('дым', 'дымка', 2)
        self.assert_ld('выстригать', 'стриж', 6)
        self.assert_ld('собака', 'сабака', 1)


if __name__ == '__main__':
    unittest.main()
