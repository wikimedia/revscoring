import re
import warnings

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("spanish")
STOPWORDS = set(stopwords.words("spanish"))
BAD_REGEXES = [
    'ano',
    'bastardo', 'bollo', 'boludo', 'bugarr[óo]n',
    'ca(gar(ro)?|ca)', 'cabr[óo]n', 'cacas', 'capullo', 'carajo',
        'chingar', 'chino', 'choch[oa]', 'cholo', 'chucha', 'chupar',
        'chupapollas', 'chupamedias', 'cipote', 'clamidia', 'coger',
        'cojones', 'concha', 'conejo', 'consolador', 'coño', 'cuca',
        'culear', 'culo', 'cundango',
    'drogata',
    'facha', 'follar', 'fornicar', 'fulana', 'furcia',
    'gabacho', 'gay', 'gilipollas', 'gitano', 'gonorrea', 'gordo',
        'gringo', 'guiri',
    'herpes', 'homosexual', 'huevos', '(huev|we)[óo]n',
    'imb[ée]cil',
    'japo', 'joder', 'joto', 'jud[íi]o',
    'lesbiana',
    'mach(orra|etorra)', 'maldito', 'mamada', 'manola',
        'maric(a|[óo]n)', 'marimach[ao]', 'maripos[óo]n',
        'mea(r|da)', 'mam[óo]n', 'mierda', 'minga', 'moro',
    'nazi', 'negrata',
    'ojete',
    'paja', 'paki', 'pedo', 'pelao', 'pelotas', 'pendejo', 'pene', 'picha',
        'pinche', 'pito', 'polla', 'polvo', 'poto', 'prostituta', 'put[ao]',
        'puñal',
    'rabo', 'ramera',
    'sida', 'skin(head)?', 'subnormal', 'sudaca', 's[íi]filis',
    'tonto', 'torta', 'tortillera', 'tranca', 'tranny',
        'travesti', 'travolo', 'trolo',
    'verga', 'vibrador', 'vulva',
    'zapatona', 'zorra'
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
DICTIONARY = enchant.Dict("es")

def stem_word_process():
    def stem_word(word):
        return STEMMER.stem(word).lower()
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process)

def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process)

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process)

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process)

spanish = Language("revscoring.languages.spanish",
                   [stem_word, is_badword, is_misspelled, is_stopword])
