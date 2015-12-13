REPLACEMENT_CHAR = "\uFFFD"


def token_is_word(t):
    return t.type == "word"


def utf16_cleanup(token):
    """
    Removes chars that can't be represented in two bytes.  This is important
    since `enchant` will expect that all strings passed to it are two-byte
    chars and print "This UTF-8 encoding can't convert to UTF-16:" if it can't
    decode.  This prevents that problem.
    See https://github.com/rfk/pyenchant/issues/58
    """
    return "".join(c if ord(c) < 2**16 else REPLACEMENT_CHAR
                   for c in token)
