from revscoring.utilities.fetch_idioms import is_idiom


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
