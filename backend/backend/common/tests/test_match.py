from django.test import TestCase

from backend.common.match import match


class MatchTestCase(TestCase):
    def test_match_chars_only(self):
        self.assertTrue(match(r'ab', 'ab'))

    def test_match_chars_only_fail(self):
        self.assertFalse(match(r'ab', 'ac'))

    def test_match_star_only_empty(self):
        self.assertTrue(match(r'.*', ''))

    def test_match_star_only_single(self):
        self.assertTrue(match(r'.*', 'a'))

    def test_match_star_only_many(self):
        self.assertTrue(match(r'.*', 'abcd'))

    def test_match_plus_only_empty(self):
        self.assertFalse(match(r'.+', ''))

    def test_match_plus_only_single(self):
        self.assertTrue(match(r'.+', 'a'))

    def test_match_plus_only_many(self):
        self.assertTrue(match(r'.+', 'abcd'))

    def test_plus_bounded(self):
        self.assertTrue(match(r'|.+|', '|aa|'))

    def test_plus_specific_bounded(self):
        self.assertTrue(match(r'|a+|', '|aa|'))
