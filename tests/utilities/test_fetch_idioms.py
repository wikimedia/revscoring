from collections import OrderedDict

from revscoring.utilities.fetch_idioms import create_regex, is_idiom, \
    construct_trie, convert_trie_to_regex


def test_is_idiom():
    phrases = [
        'Appendix:English 19th Century idioms',
        'about to',
        'activist justice',
        'attaboy',
        'bat for the other team',
        'beard the lion in his den',
        'as gentle as a dove',
        'I\'ll say'
    ]
    idioms = [phrase for phrase in phrases if is_idiom(phrase)]

    assert idioms == ['bat for the other team', 'beard the lion in his den']


def test_construct_trie():
    words = ['gold', 'goat', 'goal', 'sole']
    trie = construct_trie(words)
    assert trie == OrderedDict({
        "g": {
            "o": {
                "l": {
                    "d": {}
                },
                "a": {
                    "t": {},
                    "l": {}
                }
            }
        },
        "s": {
            "o": {
                "l": {
                    "e": {}
                }
            }
        }
    })


def test_convert_trie_to_regex():
    trie = OrderedDict({'g': {'o': {'l': {'d': {}}, 'a': {'t': {}, 'l': {}}}},
                        's': {'o': {'l': {'e': {}}}}})
    regex = convert_trie_to_regex(trie)
    assert regex == '(?:go(?:ld|a(?:t|l))|sole)'


def test_create_regex():
    idioms = [
        'laugh all the way to the bank',
        'laugh one\'s head off',
        'packed to the rafters',
        'park that thought',
        'park the bus'
    ]
    regex = create_regex(idioms)

    assert regex == "(?:laugh (?:all the way to the bank|one's head off)" \
                    "|pa(?:cked to the rafters|rk th(?:at thought|e bus)))"
