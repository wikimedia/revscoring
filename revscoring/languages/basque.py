from .features import Dictionary

name = "basque"

try:
    import enchant
    dictionary = enchant.Dict("eu")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'eu'.  " +
                      "Consider installing 'hunspell-eu'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "eu". Provided by `hunspell-eu`
"""
