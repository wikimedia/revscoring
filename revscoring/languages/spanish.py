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
        'chupa(r|me|mel[ao])', 'chup[ea][nr]', 'chupen(la|me)',
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
#TODO: more badwords
"""
    chinga chingada chingen chinguen chocha chucha chupa chupaba chupaban
    chupame chupamela chupan chupar chupen chupenla chupenme chupo cojer cojio
    cojones comeme comian conchetumare coño culeros culiao culiaos culito
follaba follar follo
gays gey gilipollas guevo guey
hijueputa hijueputas holocuento
idiota idiotas imbecil
jilipollas joder joto jotos
malparido malparidos mamada mamadas mamaguevo mamon marica maricas marico
    maricon maricones merda metia meto mierda mierdaa mierdas mocos mojon monda
nacio
ojete pajas pajero
pario pattaya pedo
pedos pelan pelotudo pelotudos pendeja pendejada pendejadas pendejo pendejos peo
    peos perra perras petardas petes picha pichula pija pijas piko pinche
    pinches pinga pipi pirobos pito polla pollas poronga poto puta putaa putas
    puto puton putos sorete
teta tetas trola trolo
verga vergas violo
wea weon weones wey
zorra"""

#TODO: informal words
"""
agan
agregenme
aguante
aki
amo
amoo
amooo
amoooo
apesta
asco
att
atte
bieber
bla
bobada
bobos
cafemontevideo
chido
comia
comio
contributions
copien
cursiva
descubrio
direction
estupida
estupides
estupido
estupidos
fea
feas
feo
feos
grasias
guapo
haha
hahaha
hola
holaa
holaaa
holaaaa
holaaaaa
holi
holis
hotmail
ijos
inserta
jaja
jajaj
jajaja
jajajaj
jajajaja
jajajajaj
jajajajaja
jajajajajaja
jajajajajajaja
jajajajajajajaja
jeje
jejeje
jiji
kien
kiero
komo
lean
lees
loko
lol
malparida
mcfinnigan
mensos
metio
metroflog
minecraft
muxo
negrita
ojala
osea
pene
penes
pollid
popo
porfavor
porke
porq
porqe
porqueria
profe
pupu
qiero
redtube
saludos
satanists
sierto
soi
sophonpanich
subnormal
tambn
tanga
tonta
tonto
tontos
umaxnet
vallanse
vayanse
wena
weno
xdd
xddd
xdddd
xfarm
yolo
zorpia
"""
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
