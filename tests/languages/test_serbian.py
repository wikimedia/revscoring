import pickle
import pytest
from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import serbian

from .util import compare_extraction

BAD = [
    "геј",
    "говна",
    "говно",
    "далматии",
    "јебање",
    "јебач",
    "јебе",
    "јебем",
    "јебига",
    "јебите",
    "јебо",
    "компније",
    "лезбејка",
    "курац",
    "курца",
    "курчина",
    "мажарскога",
    "мажарску",
    "педер",
    "педери",
    "педерима",
    "педерски",
    "педеру",
    "пизда",
    "пизде",
    "пиздо",
    "пизду",
    "пичка",
    "пичке",
    "пичко",
    "пичку",
    "срање",
    "шупак",
]

INFORMAL = [
    "ђе",
    "исплњени",
    "коњу",
    "многија",
    "многими",
    "мнози",
    "покраше",
    "серба",
    "сербија",
    "сербије",
    "сербији",
    "серпска",
    "серпске",
    "серпски",
    "серпским",
    "серпског",
    "серпској",
    "серпскохрватским",
    "србске",
    "србским",
    "србских",
    "србског",
    "србској",
    "србску",
    "хабзбзрге",
    "хаха",
    "хахаха",
    "хахахаха",
    "хахахахаха",
]

OTHER = [
    """
    Мултипла склероза (МС), (лат. Sclerosis multiplex) је неуродегенеративно
    обољење и аутоимуна болест која првенствено „напада“ белу масу централног
    нервног система. Мултипла склероза захвата аксоне, дугачке продужетке
    нервне ћелије, на којима поједини делови мијелинског омотача запаљенски
    реагују и пропадају. Стога се мултипла склероза сматра запаљенском,
    демијелинизирајућом болешћу изазваном имунолошким променама непознате
    етиологије. Кад је одређени део мијелинског омотача запаљен и оштећен,
    преношење импулса кроз аксон је поремећено, успорено или испрекидано, због
    чега поруке из мозга долазе на „циљ“ са закашњењем, „грешкама“ или их
    уопште нема (изостају). Болест је врло променљивог тока, испољава се
    неуролошким симптомима и знацима и карактеришу је честа погоршања
    различитог степена, која се смењују са наглим побољшањим клиничке слике
    (ремисија болести). Настанак мултипле склерозе прате многи поремећаји
    различитог степена, од благе укочености и отежаног ходања, до потпуне
    одузетости, слепила, итд.
    """
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(serbian.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert serbian.badwords == pickle.loads(pickle.dumps(serbian.badwords))


def test_informals():
    compare_extraction(serbian.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert serbian.informals == pickle.loads(pickle.dumps(serbian.informals))


@pytest.mark.skip(reason="CI fails although local test passes ¯\_(ツ)_/¯")
def test_dictionary():
    cache = {r_text: "Стога мулплати се мултипла склероза."}
    assert (solve(serbian.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['Стога', 'се', 'мултипла', 'склероза'])
    assert (solve(serbian.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['мулплати'])

    assert (serbian.dictionary ==
            pickle.loads(pickle.dumps(serbian.dictionary)))


def test_stopwords():
    cache = {r_text: "Стога дан датум склероза."}
    assert (solve(serbian.stopwords.revision.datasources.stopwords,
                  cache=cache) ==
            ['дан', 'датум'])
    assert (solve(serbian.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['Стога', 'склероза'])

    assert serbian.stopwords == pickle.loads(pickle.dumps(serbian.stopwords))
