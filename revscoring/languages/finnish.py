from .features import RegexMatches, Stopwords

name = "finnish"

# No dictionary

# No stemmer

# Copied from https://meta.wikimedia.org/wiki/?oldid=16354094
stopwords = [
    "aakkostus", "aiheesta", "aikana", "aina", "ajan", "ajankohta", "align",
    "alkoi", "alkuperäinen", "alun", "alussa", "and", "artikkeli",
    "artikkelit", "asp", "asti", "center", "class", "com", "commons",
    "commonscat", "defaultsort", "edelleen", "eikä", "eivät", "eli",
    "elävät", "ennen", "ensimmäinen", "ensimmäisen", "eri", "esimerkiksi",
    "että", "file", "helsingin", "helsinki", "henkilöt", "historia", "htm",
    "html", "http", "hyvin", "hän", "hänen", "hänet", "ikä", "image", "index",
    "isbn", "issa", "itse", "joiden", "joissa", "joista", "joka", "jolla",
    "jolloin", "jonka", "jopa", "jos", "jossa", "josta", "jota", "jotka",
    "julkaisija", "julkaisu", "julkaisupaikka", "jälkeen", "kaikki",
    "kaksi", "kanssa", "katso", "kaupunki", "kautta", "kerran", "keskeiset",
    "kesäkuuta", "kieli", "kirjaviite", "koko", "kolme", "korjattava", "koska",
    "kotisivu", "kuin", "kuitenkaan", "kuitenkin", "kun", "kuolleet", "kuten",
    "kuuluu", "kuva", "kuvateksti", "käyttää", "left", "leveys", "link",
    "lippu", "lisäksi", "lla", "lle", "logo", "lokakuuta", "luettelo", "luku",
    "luokka", "luvulla", "luvun", "lähde", "lähes", "lähteet", "lähteetön",
    "lähtien", "maa", "maaliskuuta", "mikä", "muassa", "muiden", "muita",
    "mukaan", "mukana", "mutta", "muualla", "muun", "muut", "myöhemmin",
    "myös", "name", "nbsp", "neljä", "net", "news", "niiden", "niin",
    "nimeke", "nimellä", "nimi", "noin", "nykyään", "näin", "ohjaus", "old",
    "ole", "olevan", "oli", "olisi", "olivat", "olla", "ollut", "org", "osa",
    "osoite", "ovat", "paljon", "pdf", "php", "png", "ref", "references",
    "right", "rivi", "saa", "saanut", "sai", "samalla", "sanomat", "sekä",
    "selite", "sen", "seulonnan", "siihen", "siitä", "sillä", "sitä", "sivu",
    "sivut", "ssa", "ssä", "sta", "style", "suomalainen", "suomalaiset",
    "suomen", "suomessa", "suomi", "suuri", "suurin", "svg", "syntyneet",
    "syyskuuta", "taas", "tai", "tammikuuta", "tarkoittaa", "teki", "tekijä",
    "teksti", "the", "thumb", "tiedosto", "tiedostomuoto", "title", "toimi",
    "toimii", "toinen", "toisen", "tulee", "tuli", "tunniste", "tynkä",
    "tyyppi", "tämä", "tämän", "usein", "useita", "uuden", "uusi", "uutiset",
    "vaan", "vaikka", "vain", "vasta", "vastaan", "verkkoviite", "vielä",
    "viitattu", "viitteet", "virallinen", "voi", "voidaan", "vuoden",
    "vuodesta", "vuoksi", "vuonna", "vuosi", "vuosina", "vuoteen", "vuotta",
    "world", "www", "yhdessä", "yhdysvallat", "yhdysvaltain", "yhteensä",
    "yksi", "yle", "yleensä", "yli",
]
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
"common words" in https://meta.wikimedia.org/wiki/?oldid=16354094
"""

stopwords = Stopwords(name + ".stopwords", stopwords)

badword_regexes = [
    r"homo",
    r"homoja",
    r"homot",
    r"hintti",
    r"homppeli",
    r"huora",
    r"idiootti",
    r"jumalauta",
    r"juntti",
    r"kakka",
    r"kakkaa",
    r"kikkeli",
    r"kyrpä",
    r"kulli",
    r"kusi",
    r"kusipää",
    r"läski",
    r"mamu",
    r"matu",
    r"neekeri",
    r"nussii",
    r"narttu",
    r"paska",
    r"paskaa",
    r"paskat",
    r"paskin",
    r"paskova",
    r"pelle",
    r"perse",
    r"perseeseen",
    r"perseessä",
    r"perseestä",
    r"perseenreikä",
    r"perkele",
    r"pillu",
    r"pilluun",
    r"pippeli",
    r"pieru",
    r"retardi",
    r"runkkari",
    r"saatana",
    r"saatanan",
    r"tyhmä",
    r"vammane",
    r"vammanen",
    r"vittu",
    r"vitun",
    r"äpärä"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"haistakaa",
    r"imekää",
    r"lol",
    r"ootte",
    r"moi",
    r"hei",
    r"sinä",
    r"sä",
    r"minä",
    r"mää",
    r"ok",
    r"joo",
    r"okei"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
