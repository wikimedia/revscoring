"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `str`'s or `list` ( `str` ) and extract information from them.

.. autoclass:: revscoring.datasources.meta.extractors.regex

"""
import re

from ..datasource import Datasource


class regex(Datasource):
    """
    Generates a list of strings that match any of a set of privided `regexes`

    :Parameters:
        regexes : `list` ( `str` )
            A list of regexes to find in the text
        text_datasource : :class:`revscoring.Datasource`
            A datasource that returns a `str` or a `list` of `str`
        regex_flags : `int`
            A set of regex flags to use in matching
        name : `str`
            A name for the new datasource
    """
    def __init__(self, regexes, text_datasource, regex_flags=re.I, name=None):
        group_pattern = r"\b(" + r"|".join(regexes) + r")\b"
        self.group_re = re.compile(group_pattern, flags=regex_flags)
        name = self._format_name(name, [regexes, text_datasource])
        super().__init__(name, self.process, depends_on=[text_datasource])

    def process(self, text_or_texts):
        if text_or_texts is None:
            return []
        elif isinstance(text_or_texts, str):
            text = text_or_texts
            return [match.group(0) for match in self.group_re.finditer(text)]
        else:
            texts = text_or_texts
            return [match.group(0)
                    for text in texts
                    for match in self.group_re.finditer(text)]
