import re
import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from .language import RegexLanguage

stemmer = SnowballStemmer("spanish")
stopwords = set(stopwords.words("spanish"))
badwords = [
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
informals = [
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

try:
    dictionary = enchant.Dict("es")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'es'.  " +
                      "Consider installing 'myspell-es'.")

sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    informals=informals,
    dictionary=dictionary,
    stemmer=stemmer,
    stopwords=stopwords
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for Spanish.
Comes complete with all language utilities.
"""
