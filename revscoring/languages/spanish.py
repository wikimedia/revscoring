import re
import warnings

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import Language, LanguageUtility

STEMMER = SnowballStemmer("spanish")
STOPWORDS = set(stopwords.words("spanish"))
BAD_REGEXES = [
    'ano', 'amaona', 'autofellation', 'aweonao',
    'bastardo', 'bollo', 'boludo', 'bugarr[óo]n',
    'ca(gar(ro)?|ca)', 'cabr[óo]n(es)?', 'caca', 'caga(d[ao]|r)?', 'capullo',
        'cagaro?', 'carajo',
        'chinga(r|da)?', 'chingu?en', 'chino', 'choch[oa]', 'cholo', 'chucha',
        'chupa(r|me|mel[ao]|ban?)?', 'chup[ea][nr]', 'chupen(la|me)', 'chupo',
        'chupapollas', 'chupamedias', 'cipote', 'clamidia', 'co[gj]er', 'cojio',
        'cojones', 'comeme', 'comian', 'conch(a|etumare)', 'conejo',
        'consolador', 'co[ñn]o', 'cuca',
        'cule(ar|ros)', 'culito', 'cul(o|iaos?)', 'cundango',
    'drogata',
    'facha', 'folla(r|ba)', 'follo', 'fornicar', 'fulana', 'furcia',
    'gabacho', 'g[ae]ys?', 'gilipollas', 'gitano', 'gonorrea', 'gordo',
        'gringo', 'gue(vo|y)', 'guiri',
    'herpes', 'homosexual', 'huevos', '(huev|we)[óo]n', 'hijueputas?',
        'holocuento',
    'idiotas?', 'imb[ée]cil',
    'japo', 'joder', 'jotos?', 'jud[íi]o',
    'lesbiana',
    'mach(orra|etorra)', 'maldito', 'malparido', 'mama(da|guevo)', 'mamon',
        'manola', 'maric(a|[óo]n)', 'marimach[ao]', 'maripos[óo]n',
        'mea(r|da+)s?', 'mam[óo]+n', 'mierda', 'minga', 'mocos', 'mojon',
        'monda', 'moro',
    'nacio', 'nazi', 'negrata',
    'ojete',
    'pajas?', 'pajero', 'pario', 'paki', 'pedo', 'pelao', 'pelotas',
        'pendej(o|a|ada)s?',
        'pene', 'peos?', 'pich(a|ula)', 'pijas?', 'piko',
        'pinches?', 'pinga', 'pipi', 'pirobos', 'pito', 'pollas?', 'poronga',
        'polvo', 'poto', 'prostituta', 'put[ao]+(s|n)?',
        'puñal',
    'rabo', 'ramera',
    'sida', 'skin(head)?', 'sorete', 'subnormal', 'sudaca', 's[íi]filis',
    'tetas?', 'tonto', 'torta', 'tortillera', 'tranca', 'tranny',
        'travesti', 'travolo', 'trol(o|a)',
    'vergas?', 'vibrador', 'violo', 'vulva',
    'wea', 'weon(es)?', 'wey',
    'zapatona', 'zorra'
]
INFORMAL_REGEXES = [
    'agan', 'agregenme', 'aguante', 'aki', 'amo', 'amoo', 'amooo', 'amoooo',
        'apesta', 'asco', 'att', 'atte',
    'bieber', 'bla', 'bobada', 'bobos',
    'cafemontevideo', 'chido', 'comia', 'comio', 'contributions', 'copien',
        'cursiva',
    'descubrio', 'direction',
    'estupida', 'estupides', 'estupido', 'estupidos',
    'fea', 'feas', 'feo', 'feos',
    'grasias', 'guapo',
    'haha', 'hahaha', 'hola+', 'holis?', 'hotmail',
    'ijos', 'inserta',
    '(ja)+', '(je)+', '(ji)+',
    'kie(n|ro)', 'komo',
    'lean', 'lees', 'loko', 'lol',
    'malparida', 'mcfinnigan', 'mensos', 'metio', 'metroflog', 'minecraft',
        'muxo', 'negrita',
    'ojala', 'osea',
    'pene', 'penes', 'pollid', 'popo', 'porfavor', 'porke', 'porq', 'porqe',
        'porqueria', 'profe', 'pupu',
    'qiero',
    'redtube',
    'saludos', 'satanists', 'sierto', 'soi', 'sophonpanich', 'subnormal',
    'tambn', 'tanga', 'tonta', 'tonto', 'tontos',
    'umaxnet',
    'vallanse', 'vayanse',
    'wena', 'weno',
    'xd+', 'xfarm',
    'yolo',
    'zorpia'
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
INFORMAL_REGEX = re.compile("|".join(INFORMAL_REGEXES))
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

def is_informal_word_process():
    def is_informal_word(word):
        return bool(INFORMAL_REGEX.match(word.lower()))
    return is_informal_word
is_informal_word = LanguageUtility("is_informal_word",
    is_informal_word_process, depends_on=[])

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
                   [stem_word, is_badword, is_informal_word, is_misspelled,
                    is_stopword])
