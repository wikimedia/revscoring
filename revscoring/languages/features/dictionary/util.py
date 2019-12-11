import enchant

REPLACEMENT_CHAR = "\uFFFD"


def utf16_cleanup(token):
    """
    Removes chars that can't be represented in two bytes.  This is important
    since `enchant` will expect that all strings passed to it are two-byte
    chars and print "This UTF-8 encoding can't convert to UTF-16:" if it can't
    decode.  This prevents that problem.
    See https://github.com/rfk/pyenchant/issues/58
    """
    return "".join(c if ord(c) < 2 ** 16 else REPLACEMENT_CHAR
                   for c in token)


def load_dict(dict_name, target_package):
    try:
        return enchant.Dict(dict_name)
    except enchant.errors.DictNotFoundError:
        raise ImportError(
            ("No enchant-compatible dictionary found for {0!r}.  " +
             "Consider installing {1!r}").format(dict_name, target_package))


class MultiDictChecker:
    """
    Implements a check() method that will iterate through dictionaries looking
    for any correct spelling.
    """

    def __init__(self, *dicts):
        self.dicts = dicts

    def check(self, word):
        for dict in self.dicts:
            if dict.check(word):
                return True
        return False
