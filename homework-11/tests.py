import unittest
from levenshtein import get_levenshtein_distance as ld


class TestLevenshteinDistance(unittest.TestCase):
    def assert_levenshtein_distance(self, a, b, result):
        self.assertEqual(ld(a, b), result)
        self.assertEqual(ld(b, a), result)

    def test_two_empty_strings(self):
        self.assert_levenshtein_distance('', '', 0)

    def test_one_empty_strings(self):
        self.assert_levenshtein_distance('', 'дом', 3)
        self.assert_levenshtein_distance('', 'дорога', 6)

    def test_lowercase_uppercase(self):
        self.assert_levenshtein_distance('cтрока', 'СТРОКА', 6)
        self.assert_levenshtein_distance('собака', 'СОБАКА', 6)
        self.assert_levenshtein_distance('дом', 'ДОМ', 3)    

    def test_equal_words(self):
        self.assert_levenshtein_distance('cтрока', 'cтрока', 0)
        self.assert_levenshtein_distance('собака', 'собака', 0)
        self.assert_levenshtein_distance('СОБАКА', 'СОБАКА', 0)
        self.assert_levenshtein_distance('дорога', 'дорога', 0)
        self.assert_levenshtein_distance('перегрузить', 'перегрузить', 0)

    def test_different_words(self):
        self.assert_levenshtein_distance('cтрока', 'собака', 4)
        self.assert_levenshtein_distance('природный', 'бездомник', 7)
        self.assert_levenshtein_distance('богомильство', 'преграждение', 12)
        self.assert_levenshtein_distance('перегрузить', 'перестройка', 7)
        self.assert_levenshtein_distance('дым', 'дымка', 2)
        self.assert_levenshtein_distance('выстригать', 'стриж', 6)
        self.assert_levenshtein_distance('собака', 'сабака', 1)


if __name__ == '__main__':
    unittest.main()
