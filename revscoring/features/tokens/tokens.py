

class Tokens:

    def __init__(self, prefix, tokens):

        self.tokens = tokens
        """
        A list of tokens
        """

        self.numbers = self.tokens_in_types(
            {'number'},
            name=prefix + ".numbers"
        )
        """
        A list of numeric tokens
        """

        self.numbers_frequency = frequencies.table(
            self.numbers,
            name=prefix + ".numbers_frequency"
        )
        """
        A frequency table of number tokens.
        """

        self.whitespaces = self.tokens_in_types(
            {'whitespace'},
            name=prefix + ".whitespaces"
        )
        """
        Returns a list of whitespace tokens
        """

        self.whitespace_frequency = frequencies.table(
            self.whitespaces,
            name=prefix + ".whitespace_frequency"
        )
        """
        A frequency table of whichspace tokens.
        """

        self.markups = self.tokens_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=prefix + ".markups"
        )
        """
        Returns a list of markup tokens
        """

        self.markup_frequency = frequencies.table(
            self.markups,
            name=prefix + ".markup_frequency"
        )
        """
        A frequency table of markup tokens.
        """

        self.cjks = self.tokens_in_types(
            {'cjk'},
            name=prefix + ".cjks"
        )
        """
        Returns a list of Chinese/Japanese/Korean tokens
        """

        self.cjk_frequency = frequencies.table(
            self.cjks,
            name=prefix + ".cjk_frequency"
        )
        """
        A frequency table of cjk tokens.
        """

        self.entitys = self.tokens_in_types(
            {'entity'},
            name=prefix + ".entitys"
        )
        """
        Returns a list of HTML entity tokens
        """

        self.entity_frequency = frequencies.table(
            self.entitys,
            name=prefix + ".entity_frequency"
        )
        """
        A frequency table of entity tokens.
        """

        self.urls = self.tokens_in_types(
            {'url'},
            name=prefix + ".urls"
        )
        """
        Returns a list of URL tokens
        """

        self.url_frequency = frequencies.table(
            self.urls,
            name=self.prefix + ".url_frequency"
        )
        """
        A frequency table of url tokens.
        """

        self.words = self.tokens_in_types(
            {'word'},
            name=self.prefix + ".words"
        )
        """
        Returns a list of word tokens
        """

        self.word_frequency = frequencies.table(
            self.words,
            name=self.prefix + ".word_frequency"
        )
        """
        A frequency table of word tokens.
        """

        self.punctuations = self.tokens_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon'},
            name=self.prefix + ".punctuations"
        )
        """
        Returns a list of punctuation tokens
        """

        self.punctuation_frequency = frequencies.table(
            self.punctuations,
            name=self.prefix + ".punctuation_frequency"
        )
        """
        A frequency table of punctuation tokens.
        """

        self.breaks = self.tokens_in_types(
            {'break'},
            name=self.prefix + ".breaks"
        )
        """
        Returns a list of break tokens
        """

        self.break_frequency = frequencies.table(
            self.breaks,
            name=self.prefix + ".break_frequency"
        )
        """
        A frequency table of break tokens.
        """

    def tokens_in_types(types, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all content
        tokens that are within a set of types.
        """
        types = set(types)

        if name is None:
            name = "{0}({1})" \
                   .format("tokens_in_types", types)

        return filter(lambda t: t.type in types, self.tokens, name=name)

    def tokens_matching(regex, name=None, regex_flags=re.I):
        """
        Constructs a :class:`revscoring.Datasource` that returns all content
        tokens that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)

        if name is None:
            name = "{0}({1})".format("tokens_matching", regex.pattern)

        return regex_matching(regex, self.tokens, name=name)
