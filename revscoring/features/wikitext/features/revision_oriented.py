from revscoring.dependencies import DependentSet

from . import chars, edit_tokens, parsed, tokenized

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
            """
            :class:`revscoring.features.wikitext.Revision` : The
            parent (aka "previous") revision of the page.
            """

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(
                name + ".diff",
                self.datasources.diff
            )
            """
            :class:`~revscoring.features.wikitext.Diff` : The
            difference between this revision and the parent revision.
            """


class Revision(parsed.Revision, chars.Revision, tokenized.Revision,
               BaseRevision):
    pass


class BaseDiff(DependentSet):

    def __init__(self, name, diff_datasources, *args, **kwargs):
        super().__init__(name)
        self.datasources = diff_datasources


class Diff(chars.Diff, edit_tokens.Diff, tokenized.Diff, BaseDiff):
    pass
