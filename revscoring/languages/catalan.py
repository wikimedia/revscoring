from .features import Dictionary, RegexMatches

name = "catalan"

try:
    import enchant
    dictionary = enchant.Dict("ca")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'ca'.  " +
                      "Consider installing 'myspell-ca'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
`enchant.Dict <https://github.com/rfk/pyenchant>`_ "ca".  Provided by `myspell-ca`
"""

badword_regexes = [
    r'cabron',
    r'cabrones',
    r'caca',
    r'caga',
    r'cagar',
    r'cago',
    r'capullo',
    r'catalufo',
    r'catalufos',
    r'cojones',
    r'cony',
    r'coño',
    r'choch[oa]',
    r'chup[ea][nr]',
    r'chupa(r|me|mel[ao]|ban?)?',
    r'cul',
    r'culito',
    r'culo',
    r'coi',
    r'facha',
    r'fatxa',
    r'folla',
    r'follar',
    r'follen',
    r'gay',
    r'gilipollas',
    r'gordo',
    r'gorda',
    r'guarra',
    r'imbecil',
    r'imbècil',
    r'joder',
    r'maricon',
    r'marimach[ao]',
    r'maripos[óo]n',
    r'mea(r|da+?)s?',
    r'merda',
    r'merdas',
    r'merdes',
    r'mierda',
    r'mierdas',
    r'minga',
    r'mocos',
    r'mojon',
    r'moro',
    r'negrata',
    r'paja',
    r'pajero',
    r'paki',
    r'pedo',
    r'pene',
    r'penes',
    r'penis',
    r'pipi',
    r'polla',
    r'pollas',
    r'polles',
    r'popo',
    r'porno',
    r'puta',
    r'putas',
    r'putes',
    r'puticlub',
    r'puto',
    r'putos',
    r'rabo',
    r'ramera',
    r'separata',
    r'subnormal',
    r'tonta',
    r'tonto',
    r'tontos',
    r'trol(o|a)',
    r'vergas?',
    r'vibrador',
    r'xdd',
    r'xddd',
    r'zorra',
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r'asi',
    r'bienvenido',
    r'bienvenidos',
    r'esto',
    r'estúpid',
    r'jaja',
    r'jajaja',
    r'jajajaja',
    r'(ha)+',
    r'(he)+',
    r'hola',
    r'holi',
    r'hosti',
    r'hostia',
    r'hòstia',
    r'ignorant',
    r'llamo',
    r'lol',
    r'malparit',
    r'mua(ha)+',
    r'merci',
    r'nadie',
    r'osti',
    r'quede',
    r'quereis',
    r'resto',
    r'soy',
    r'traga',
    r'tranqui',
    r'visca',
    r'viva',
    r'vuestros',
    r'xd',
    r'xupa',
    r'wtf',
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
