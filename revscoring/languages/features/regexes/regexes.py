from ....datasources import revision_oriented
from .revision_oriented import RegexesDiff, RegexesRevision


class Regexes:

    def __init__(self, prefix, regexes):

        self.revision = RegexesRevision(
            prefix + ".revision", regexes,
            revision_oriented.revision.text,
            revision_oriented.revision.parent.text
        )

        self.diff = RegexesDiff(
            prefix + ".diff", regexes,
            self.revision.datasources,
            self.revision.parent.datasources
        )
