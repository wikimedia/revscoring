from revscoring.utilities.fetch_idioms import create_regexes, is_idiom


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


def test_create_regexes():
    idioms = [
        'laugh all the way to the bank',
        'laugh one\'s head off',
        'packed to the rafters',
        'park that thought',
        'park the bus'
    ]
    regexes = create_regexes(idioms)

    assert regexes == ['laugh (all the way to the bank|one\'s head off)',
                       'packed to the rafters', 'park (that thought|the bus)']
