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
        wrapping : ( `str`, `str` )
            Wrap all regexes with these values.  This is useful for languages
            that *have* word boundaries.
        name : `str`
            A name for the new datasource
    """
    def __init__(self, regexes, text_datasource, regex_flags=re.I,
                 wrapping=(r'\b', r'\b'), exclusions=None, name=None):
        wrapping = wrapping or ("", "")
        group_pattern = r"(" + wrapping[0] + r")" + \
                        r"(" + r"|".join(regexes) + r")" + \
                        r"(" + wrapping[1] + r")"
        self.group_re = re.compile(group_pattern, flags=regex_flags)
        if exclusions is not None:
            exclusion_pattern = r"(" + wrapping[0] + r")" + \
                                r"(" + r"|".join(exclusions) + r")" + \
                                r"(" + wrapping[1] + r")"
            self.exclude_re = re.compile(exclusion_pattern, flags=regex_flags)
        else:
            self.exclude_re = None

        name = self._format_name(name, [regexes, text_datasource])
        super().__init__(name, self.process, depends_on=[text_datasource])

    def process(self, text_or_texts):
        if text_or_texts is None:
            return []
        elif isinstance(text_or_texts, str):
            text = text_or_texts
            return [match.group(2)
                    for match in self.group_re.finditer(text)
                    if not hasattr(self, 'exclude_re') or
                       self.exclude_re is None or
                       not self.exclude_re.match(match.group(2))]
        else:
            texts = text_or_texts
            return [match.group(2)
                    for text in texts
                    for match in self.group_re.finditer(text)
                    if not hasattr(self, 'exclude_re') or
                       self.exclude_re is None or
                       not self.exclude_re.match(match.group(2))]
