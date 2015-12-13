import re

from ..datasource import Datasource


class regextract(Datasource):
    """
    Abstract base-class that represents a Regex extractor.
    """
    def __init__(self, regexes, text_datasource, regex_flags=re.I, name=None):
        group_pattern = r"\b(" + r"|".join(regexes) + r")\b"
        self.group_re = re.compile(group_pattern, flags=regex_flags)
        name = self.format_name(name, [regexes, text_datasource])
        super().__init__(name, depends_on=[text_datasource])

    def process(self, text_or_texts):
        if isinstance(text_or_texts, str):
            text = text_or_texts
            return [match.group(0) for match in self.group_re.finditer(text)]
        else:
            texts = text_or_texts
            return [match.group(0)
                    for text in texts
                    for match in self.group_re.finditer(text)]
