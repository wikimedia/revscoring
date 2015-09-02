import re

from ...datasources import Datasource


class RegexExtractor(Datasource):

    def __init__(self, name, regexes, depends_on=None, if_none=None):
        super().__init__(name, self.process, depends_on=depends_on)
        group_pattern = r"\b(" + r"|".join(regexes) + r")\b"
        self.group_re = re.compile(group_pattern, flags=re.I)
        self.if_none = if_none

    def process(self, input):
        if input is None:
            if self.if_none is not None:
                self.if_none()
            else:
                return []
        else:
            return self._process(input)

    def _process(self, input):
        raise NotImplementedError()


class SegmentRegexExtractor(RegexExtractor):

    def __init__(self, name, segment_source, regexes, if_none=None):
        super().__init__(name, regexes, depends_on=[segment_source])

    def _process(self, segments):
        return [match.group(0)
                for segment in segments
                for match in self.group_re.finditer(segment)]


class TextRegexExtractor(RegexExtractor):

    def __init__(self, name, text_source, regexes, if_none=None):
        super().__init__(name, regexes, depends_on=[text_source])

    def _process(self, text):
        matches = [match.group(0)
                   for match in self.group_re.finditer(text)]
        return matches
