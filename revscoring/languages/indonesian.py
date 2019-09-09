from .features import Dictionary, RegexMatches, Stopwords

name = "indonesian"

try:
    import enchant
    dictionary = enchant.Dict("id")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'id'.  " +
                      "Consider installing 'aspell-id'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "id".  Provided by `aspell-it`
"""

# STOPWORDS from https://code.google.com/p/stop-words/source/browse/trunk/
#                stop-words/stop-words-collection-2014.02.24/stop-words/
#                stop-words_indonesian_1_id.txt
stopwords = set([
    r"ada", r"adanya", r"adalah", r"adapun", r"agak", r"agaknya", r"agar",
    r"akan", r"akankah", r"akhirnya", r"aku", r"akulah", r"amat",
    r"amatlah", r"anda", r"andalah", r"antar", r"diantaranya", r"antara",
    r"antaranya", r"diantara", r"apa", r"apaan", r"mengapa", r"apabila",
    r"apakah", r"apalagi", r"apatah", r"atau", r"ataukah", r"ataupun",
    r"bagai", r"bagaikan", r"sebagai", r"sebagainya", r"bagaimana",
    r"bagaimanapun", r"sebagaimana", r"bagaimanakah", r"bagi",
    r"bahkan", r"bahwa", r"bahwasanya", r"sebaliknya", r"banyak",
    r"sebanyak", r"beberapa", r"seberapa", r"begini", r"beginian",
    r"beginikah", r"beginilah", r"sebegini", r"begitu", r"begitukah",
    r"begitulah", r"begitupun", r"sebegitu", r"belum", r"belumlah",
    r"sebelum", r"sebelumnya", r"sebenarnya", r"berapa", r"berapakah",
    r"berapalah", r"berapapun", r"betulkah", r"sebetulnya", r"biasa",
    r"biasanya", r"bila", r"bilakah", r"bisa", r"bisakah", r"sebisanya",
    r"boleh", r"bolehkah", r"bolehlah", r"buat", r"bukan", r"bukankah",
    r"bukanlah", r"bukannya",
    r"cuma", r"percuma",
    r"dahulu", r"dalam", r"dan", r"dapat", r"dari", r"daripada", r"dekat",
    r"demi", r"demikian", r"demikianlah", r"sedemikian", r"dengan",
    r"depan", r"di", r"dia", r"dialah", r"dini", r"diri", r"dirinya",
    r"terdiri", r"dong", r"dulu",
    r"enggak", r"enggaknya", r"entah", r"entahlah",
    r"terhadap", r"terhadapnya", r"hal", r"hampir", r"hanya", r"hanyalah",
    r"harus", r"haruslah", r"harusnya", r"seharusnya", r"hendak",
    r"hendaklah", r"hendaknya", r"hingga", r"sehingga",
    r"ia", r"ialah", r"ibarat", r"ingin", r"inginkah", r"inginkan", r"ini",
    r"inikah", r"inilah", r"itu", r"itukah", r"itulah",
    r"jangan", r"jangankan", r"janganlah", r"jika", r"jikalau", r"juga",
    r"justru",
    r"kala", r"kalau", r"kalaulah", r"kalaupun", r"kalian", r"kami",
    r"kamilah", r"kamu", r"kamulah", r"kan", r"kapan", r"kapankah",
    r"kapanpun", r"dikarenakan", r"karena", r"karenanya", r"ke", r"kecil",
    r"kemudian", r"kenapa", r"kepada", r"kepadanya", r"ketika",
    r"seketika", r"khususnya", r"kini", r"kinilah", r"kiranya",
    r"sekiranya", r"kita", r"kitalah", r"kok",
    r"lagi", r"lagian", r"selagi", r"lah", r"lain", r"lainnya", r"melainkan",
    r"selaku", r"lalu", r"melalui", r"terlalu", r"lama", r"lamanya",
    r"selama", r"selama", r"selamanya", r"lebih", r"terlebih",
    r"bermacam", r"macam", r"semacam", r"maka", r"makanya", r"makin",
    r"malah", r"malahan", r"mampu", r"mampukah", r"mana", r"manakala",
    r"manalagi", r"masih", r"masihkah", r"semasih", r"masing", r"mau",
    r"maupun", r"semaunya", r"memang", r"mereka", r"merekalah", r"meski",
    r"meskipun", r"semula", r"mungkin", r"mungkinkah",
    r"nah", r"namun", r"nanti", r"nantinya", r"nyaris",
    r"oleh", r"olehnya", r"seorang", r"seseorang",
    r"pada", r"padanya", r"padahal", r"paling", r"sepanjang", r"pantas",
    r"sepantasnya", r"sepantasnyalah", r"para", r"pasti", r"pastilah",
    r"per", r"pernah", r"pula", r"pun",
    r"merupakan", r"rupanya", r"serupa",
    r"saat", r"saatnya", r"sesaat", r"saja", r"sajalah",
    r"saling", r"bersama", r"sama", r"sesama", r"sambil", r"sampai",
    r"sana", r"sangat", r"sangatlah", r"saya", r"sayalah", r"se", r"sebab",
    r"sebabnya", r"sebuah", r"tersebut", r"tersebutlah", r"sedang",
    r"sedangkan", r"sedikit", r"sedikitnya", r"segala", r"segalanya",
    r"segera", r"sesegera", r"sejak", r"sejenak", r"sekali",
    r"sekalian", r"sekalipun", r"sesekali", r"sekaligus",
    r"sekarang", r"sekarang", r"sekitar", r"sekitarnya", r"sela",
    r"selain", r"selalu", r"seluruh", r"seluruhnya", r"semakin",
    r"sementara", r"sempat", r"semua", r"semuanya", r"sendiri",
    r"sendirinya", r"seolah", r"seperti", r"sepertinya", r"sering",
    r"seringnya", r"serta", r"siapa", r"siapakah", r"siapapun", r"disini",
    r"disinilah", r"sini", r"sinilah", r"sesuatu", r"sesuatunya", r"suatu",
    r"sesudah", r"sesudahnya", r"sudah", r"sudahkah", r"sudahlah",
    r"supaya",
    r"tadi", r"tadinya", r"tak", r"tanpa", r"setelah", r"telah", r"tentang",
    r"tentu", r"tentulah", r"tentunya", r"tertentu", r"seterusnya",
    r"tapi", r"tetapi", r"setiap", r"tiap", r"setidaknya", r"tidak",
    r"tidakkah", r"tidaklah", r"toh",
    r"waduh", r"wah", r"wahai", r"sewaktu", r"walau", r"walaupun", r"wong",
    r"yaitu", r"yakni", r"yang"
])

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features provided by
https://code.google.com/p/stop-words/source/browse/trunk/\
stop-words/stop-words-collection-2014.02.24/stop-words/\
stop-words_indonesian_1_id.txt
"""

badword_regexes = [
    r"anjing",  # dog
    r"bajingan",  # crook
    r"bangsat",  # asshole / motherfucker
    r"bispak",  # whore (can be used)
    r"blo'?on",  # whacky
    r"brengse[kx]",  # useless
    r"bencong",  # transexual
    r"babi",  # swine
    r"cibai",  # smelly vagina
    r"coley",  # ???
    r"diselama",  # ???
    r"escoduro",  # ???
    r"fredrike",  # ???
    r"fogh",  # idiot (repeats mistakes)
    r"gauguin",  # ???
    r"goblok",  # fool
    r"ge[fs]tapo",  # ???
    r"husseins",  # ???
    r"indon",  # ???
    r"jambut",  # public hair
    r"jellinek",  # ???
    r"jellygamat",  # ???
    r"keparat",  # dammit
    r"kencing",  # pee
    r"kontol",  # penis
    r"kotoran",  # shit
    r"lonte",  # prostitute
    r"loked",  # crazy
    r"lvmh",  # ???
    r"malingsia",  # malaysian (slang)
    r"memek",  # pussy
    r"monyong",  # long mouth
    r"netnapa",  # ???
    r"ngentot",  # fuck
    r"nesbitt",  # ???
    r"panadta",  # ???
    r"palaji",  # ???
    r"pencuri",  # theif
    r"perek",  # slut
    r"pukimak",  # mother's cunt
    r"portugeuse",  # ???
    r"pedofil",  # pedophile
    r"riyhad",  # ???
    r"sempak",  # underwear (more like "shit" or "damn")
    r"sinting",  # crazy
    r"steinway",  # ???
    r"sukhano",  # ??? first president of Indonesia?
    r"taenjamras",  # ???
    r"tahi",  # bullshit
    r"tetek",  # breast / boobs
    r"titit",  # penis
    r"toket",  # breasts
    r"tzcesar",  # ???
    r"thailaland",  # ???
    r"thaicia"  # ???
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"hai",  # hi
    r"halo",  # hello
    r"janc[uo]k",  # closest friend
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
