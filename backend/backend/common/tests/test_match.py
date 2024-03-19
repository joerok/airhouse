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

    def test_multiple_plus(self):
        self.assertTrue(match(r'a+a+a+', 'aaa'))
        self.assertFalse(match(r'a+a+a+', 'aa'))
        self.assertTrue(match(r'a*a+a*a+a*', 'aaa'))
        self.assertFalse(match(r'a*a+a*a+a*a+', 'aa'))

    def test_assert_lots_of_backtracking(self):
        self.assertTrue(match(r'a*b*a*b*a*b*a*b*a*b*ab', 'abaabbaaabbbaaaabbbbaaaaabbbbbab'))

    def test_basic_patterns(self):
        patterns = (
            (r'a*b', 'ab', True, 'basic matching'),
            (r'a.c', 'abc', True, '. bounded by characters'),
            (r'a+b', 'aab', True, '1+ matching bounded at the end'),
            (r'', '', True, 'Empty string and empty pattern'),
            (r'a*', 'aaaaaaaa', True, 'Wildcard matches many'),
            (r'a*b', '', False, 'Empty string with bounded wildcard'),
            (r'a*', 'b', False, 'Wildcard matches only the coefficient'),
            (r'a+b', 'a', False, 'Plus bounded does not match unbounded string'),
            (r'a*b*c', 'ac', True, 'Multiple wildcards matches with bounded string'),
            (r'a*a', 'a*a', True, 'Consecutive wildcard matches with the same character'),
            (r'a*b*c*', 'aabcc', True, 'Mutiple wildcards with repetitions'),
            (r'a*b+c', 'abbc', True, 'Mixing plus and wildcards'),
            (r'a.+c', 'a1c', True, 'Any character matching'),
            (r'a*b*c', 'abca', False, 'Wildcards do not leave their bounds')
        )

        for pattern, string, result, note in patterns:
            if result == False:
                self.assertFalse(match(pattern, string), f'/{pattern}/ !~ {string} : {note}')
            else:
                self.assertTrue(match(pattern, string), f'/{pattern}/ =~ {string} : {note}')
