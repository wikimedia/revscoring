from ..feature import Feature


class string_matches(Feature):
    """
    Generates a `bool`: `True` if a string matches a regular expression and
    `False` otherwise.

    :Parameters:
        regex : `str` | `compiled re`
            A regular expression to apply to the comment
        str_datasource : :class:`revscoring.Datasource`
            A datasource that generates a `str`
        name : `str`
            A name to associate with the Feature.
    """
    def __init__(self, regex, str_datasource, name=None):
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        self.regex = regex
        name = self._format_name(name, regex, str_datasource)
        super().__init__(name, self.process, returns=bool,
                         depends_on=[str_datasource])

    def _process(self, s):
        return bool(self.regex.match(s))
