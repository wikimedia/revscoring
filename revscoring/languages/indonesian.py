import re
import warnings

import enchant

from .language import Language, LanguageUtility

# STOPWORDS from https://code.google.com/p/stop-words/source/browse/trunk/stop-words/stop-words-collection-2014.02.24/stop-words/stop-words_indonesian_1_id.txt
STOPWORDS = set([
    "ada", "adanya", "adalah", "adapun", "agak", "agaknya", "agar", "akan",
    "akankah", "akhirnya", "aku", "akulah", "amat", "amatlah", "anda",
    "andalah", "antar", "diantaranya", "antara", "antaranya", "diantara", "apa",
    "apaan", "mengapa", "apabila", "apakah", "apalagi", "apatah", "atau",
    "ataukah", "ataupun", "bagai", "bagaikan", "sebagai", "sebagainya",
    "bagaimana", "bagaimanapun", "sebagaimana", "bagaimanakah", "bagi",
    "bahkan", "bahwa", "bahwasanya", "sebaliknya", "banyak", "sebanyak",
    "beberapa", "seberapa", "begini", "beginian", "beginikah", "beginilah",
    "sebegini", "begitu", "begitukah", "begitulah", "begitupun", "sebegitu",
    "belum", "belumlah", "sebelum", "sebelumnya", "sebenarnya", "berapa",
    "berapakah", "berapalah", "berapapun", "betulkah", "sebetulnya", "biasa",
    "biasanya", "bila", "bilakah", "bisa", "bisakah", "sebisanya", "boleh",
    "bolehkah", "bolehlah", "buat", "bukan", "bukankah", "bukanlah", "bukannya",
    "cuma", "percuma", "dahulu", "dalam", "dan", "dapat", "dari", "daripada",
    "dekat", "demi", "demikian", "demikianlah", "sedemikian", "dengan", "depan",
    "di", "dia", "dialah", "dini", "diri", "dirinya", "terdiri", "dong", "dulu",
    "enggak", "enggaknya", "entah", "entahlah", "terhadap", "terhadapnya",
    "hal", "hampir", "hanya", "hanyalah", "harus", "haruslah", "harusnya",
    "seharusnya", "hendak", "hendaklah", "hendaknya", "hingga", "sehingga",
    "ia", "ialah", "ibarat", "ingin", "inginkah", "inginkan", "ini", "inikah",
    "inilah", "itu", "itukah", "itulah", "jangan", "jangankan", "janganlah",
    "jika", "jikalau", "juga", "justru", "kala", "kalau", "kalaulah",
    "kalaupun", "kalian", "kami", "kamilah", "kamu", "kamulah", "kan", "kapan",
    "kapankah", "kapanpun", "dikarenakan", "karena", "karenanya", "ke", "kecil",
    "kemudian", "kenapa", "kepada", "kepadanya", "ketika", "seketika",
    "khususnya", "kini", "kinilah", "kiranya", "sekiranya", "kita", "kitalah",
    "kok", "lagi", "lagian", "selagi", "lah", "lain", "lainnya", "melainkan",
    "selaku", "lalu", "melalui", "terlalu", "lama", "lamanya", "selama",
    "selama", "selamanya", "lebih", "terlebih", "bermacam", "macam", "semacam",
    "maka", "makanya", "makin", "malah", "malahan", "mampu", "mampukah", "mana",
    "manakala", "manalagi", "masih", "masihkah", "semasih", "masing", "mau",
    "maupun", "semaunya", "memang", "mereka", "merekalah", "meski", "meskipun",
    "semula", "mungkin", "mungkinkah", "nah", "namun", "nanti", "nantinya",
    "nyaris", "oleh", "olehnya", "seorang", "seseorang", "pada", "padanya",
    "padahal", "paling", "sepanjang", "pantas", "sepantasnya", "sepantasnyalah",
    "para", "pasti", "pastilah", "per", "pernah", "pula", "pun", "merupakan",
    "rupanya", "serupa", "saat", "saatnya", "sesaat", "saja", "sajalah",
    "saling", "bersama", "sama", "sesama", "sambil", "sampai", "sana", "sangat",
    "sangatlah", "saya", "sayalah", "se", "sebab", "sebabnya", "sebuah",
    "tersebut", "tersebutlah", "sedang", "sedangkan", "sedikit", "sedikitnya",
    "segala", "segalanya", "segera", "sesegera", "sejak", "sejenak", "sekali",
    "sekalian", "sekalipun", "sesekali", "sekaligus", "sekarang", "sekarang",
    "sekitar", "sekitarnya", "sela", "selain", "selalu", "seluruh",
    "seluruhnya", "semakin", "sementara", "sempat", "semua", "semuanya",
    "sendiri", "sendirinya", "seolah", "seperti", "sepertinya", "sering",
    "seringnya", "serta", "siapa", "siapakah", "siapapun", "disini",
    "disinilah", "sini", "sinilah", "sesuatu", "sesuatunya", "suatu",
    "sesudah", "sesudahnya", "sudah", "sudahkah", "sudahlah", "supaya",
    "tadi", "tadinya", "tak", "tanpa", "setelah", "telah", "tentang", "tentu",
    "tentulah", "tentunya", "tertentu", "seterusnya", "tapi", "tetapi",
    "setiap", "tiap", "setidaknya", "tidak", "tidakkah", "tidaklah", "toh",
    "waduh", "wah", "wahai", "sewaktu", "walau", "walaupun", "wong", "yaitu",
    "yakni", "yang"
])
BAD_REGEXES = [
    "aboput", "anjing",
    "bajingan", "bangsat", "bispak", "blo[o' ]*o?n", "brengse[kx]",
        "bishopsgarth", "bastards", "bencong", "babi"
    "cibai", "chalong", "coley",
    "diselama", "dishonest", "defraud", "defamatory",
    "escoduro",
    "fredrike", "fogh",
    "gauguin", "goblok", "ge[fs]tapo",
    "heroin", "husseins",
    "indon",
    "jambut", "janc[uo]k", "jellinek", "jellygamat",
    "keparat", "kontol",
    "lonte", "loked", "lvmh",
    "malingsia", "memek", "monyong", "munch",
    "netnapa", "ngentot", "nesbitt",
    "overdosed",
    "panadta", "palaji", "perek", "pukimak", "portugeuse", "paedophiles",
        "prostituton", "paedophile", "pedofil",
    "riyhad",
    "satanic", "satanists", "sempak", "sinting", "steinway", "sukhano",
    "terrorising", "terrorised", "terrorists", "taenjamras", "tetek", "titit",
        "toket", "tzcesar", "thailaland", "thaicia"
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
DICTIONARY = enchant.Dict("id")

def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[])

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process, depends_on=[])

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled
is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])


indonesian = Language("revscoring.languages.indonesian",
                   [is_badword, is_misspelled, is_stopword])
"""
Implements :class:`~revscoring.languages.language.Language` for Indonesian.
:data:`~revscoring.languages.language.is_badword`,
:data:`~revscoring.languages.language.is_misspelled`, and
:data:`~revscoring.languages.language.is_stopword` are provided.
"""
