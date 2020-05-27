from collections import OrderedDict

from revscoring.utilities.fetch_idioms import create_regex, is_idiom, \
    convert_trie_to_regex


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


def test_convert_trie_to_regex():
    trie = OrderedDict({'g': {'o': {'l': {'d': {}}}},
                        's': {'o': {'l': {'e': {}}}}})
    regex = convert_trie_to_regex(trie)
    assert regex in ['(?:gold|sole)', '(?:sole|gold)']


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
