from ..datasource import Datasource


class dict_keys(Datasource):
    """
    Generates a set of `dict` keys

    :Parameters:
        dict_datasource : :class:`revscoring.Datasource`
            A datasource that generates a `dict`
        name : `str`
            A name for the new datasource.
    """
    def __init__(self, dict_datasource, name=None):
        name = self._format_name(name, [dict_datasource])
        super().__init__(name, self.process,
                         depends_on=[dict_datasource])

    def process(self, d):
        return d.keys()


class dict_values(Datasource):
    """
    Generates a list of `dict` values

    :Parameters:
        dict_datasource : :class:`revscoring.Datasource`
            A datasource that generates a `dict`
        name : `str`
            A name for the new datasource.
    """
    def __init__(self, dict_datasource, name=None):
        name = self._format_name(name, [dict_datasource])
        super().__init__(name, self.process,
                         depends_on=[dict_datasource])

    def process(self, d):
        return [v for v in d.values()]
