from . import chars, edit_tokens, parsed, tokenized
from ....dependencies import DependentSet

prefix = "wikitext.revision"


class BaseRevision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        if hasattr(self.datasources, "parent"):
            self.parent = Revision(
                name + ".parent",
                self.datasources.parent
            )

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(
                name + ".diff",
                self.datasources.diff
            )


class Revision(parsed.Revision, chars.Revision, tokenized.Revision,
               BaseRevision):
    pass


class BaseDiff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources


class Diff(chars.Diff, edit_tokens.Diff, tokenized.Diff, BaseDiff):
    pass
