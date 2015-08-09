import re
import sys

import enchant
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from . import english
from .language import RegexLanguage

stemmer = SnowballStemmer("spanish")
stopwords = set(stopwords.words("spanish"))
badwords = [
    r"ano", r"amaona", r"autofellation", r"aweonao",
    r"bastardo", r"bollo", r"boludo", r"bugarr[óo]n",
    r"ca(gar(ro)?|ca)", r"cabr[óo]n(es)?", r"caca", r"caga(d[ao]|r)?",
        r"capullo", r"cagaro?", r"carajo",
        r"chinga(r|da)?", r"chingu?en", r"chino", r"choch[oa]", r"cholo",
        r"chucha", r"chupa(r|me|mel[ao]|ban?)?", r"chup[ea][nr]",
        r"chupen(la|me)", r"chupo", r"chupapollas", r"chupamedias", r"cipote",
        r"clamidia", r"co[gj]er", r"cojio", r"cojones", r"comeme", r"comian",
        r"conch(a|etumare)", r"conejo", r"consolador", r"co[ñn]o", r"cuca",
        r"cule(ar|ros)", r"culito", r"cul(o|iaos?)", r"cundango",
    r"drogata",
    r"facha", r"folla(r|ba)", r"follo", r"fornicar", r"fulana", r"furcia",
    r"gabacho", r"g[ae]ys?", r"gilipollas", r"gitano", r"gonorrea", r"gordo",
        r"gringo", r"gue(vo|y)", r"guiri",
    r"herpes", r"homosexual", r"huevos", r"(huev|we)[óo]n", r"hijueputas?",
        r"holocuento",
    r"idiotas?", r"imb[ée]cil",
    r"japo", r"joder", r"jotos?", r"jud[íi]o",
    r"lesbiana",
    r"mach(orra|etorra)", r"maldito", r"malparido", r"mama(da|guevo)", r"mamon",
        r"manola", r"maric(a|[óo]n)", r"marimach[ao]", r"maripos[óo]n",
        r"mea(r|da+)s?", r"mam[óo]+n", r"mierda", r"minga", r"mocos", r"mojon",
        r"monda", r"moro",
    r"nacio", r"nazi", r"negrata",
    r"ojete",
    r"pajas?", r"pajero", r"pario", r"paki", r"pedo", r"pelao", r"pelotas",
        r"pendej(o|a|ada)s?",
        r"pene", r"peos?", r"pich(a|ula)", r"pijas?", r"piko",
        r"pinches?", r"pinga", r"pipi", r"pirobos", r"pito", r"pollas?",
        r"poronga", r"polvo", r"poto", r"prostituta", r"put[ao]+(s|n)?",
        r"puñal",
    r"rabo", r"ramera",
    r"sida", r"skin(head)?", r"sorete", r"subnormal", r"sudaca", r"s[íi]filis",
    r"tetas?", r"tonto", r"torta", r"tortillera", r"tranca", r"tranny",
        r"travesti", r"travolo", r"trol(o|a)",
    r"vergas?", r"vibrador", r"violo", r"vulva",
    r"wea", r"weon(es)?", r"wey",
    r"zapatona", r"zorra"
]
informals = [
    r"agan", r"agregenme", r"aguante", r"aki", r"amo+",
        r"apesta", r"asco", r"att", r"atte",
    r"bieber", r"bla", r"bobada", r"bobos?",
    r"cafemontevideo", r"chido", r"comia", r"comio", r"copien",
        r"cursiva",
    r"descubrio",
    r"estupid[aeo]+[rs]?",
    r"fea", r"feas", r"feo", r"feos",
    r"grasias", r"guapo",
    r"ha(ha)+", r"hola+", r"holis?",
    r"ijos", r"inserta",
    r"(ja)+", r"(je)+", r"(ji)+",
    r"kie(n|ro)", r"komo",
    r"lean", r"lees", r"loko", r"l+o+l+",
    r"malparida", r"mcfinnigan", r"mensos", r"metio", r"metroflog", r"minecraft",
        r"muxo", r"negrita",
    r"ojala", r"osea",
    r"penes?", r"pollid", r"popo", r"porfavor", r"por[kq]e?",
        r"porqueria", r"profe", r"pupu",
    r"qiero",
    r"saludos", r"sierto", r"soi", r"sophonpanich", r"subnormal",
    r"tambn", r"tanga", r"tont[ao]+s?",
    r"umaxnet",
    r"vallanse", r"vayanse",
    r"wena", r"weno",
    r"xd+", r"xfarm",
    r"yolo",
    r"zorpia"
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
