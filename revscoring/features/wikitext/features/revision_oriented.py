from . import chars, edit_tokens, parsed, tokenized


class Revision(parsed.Revision, chars.Revision, tokenized.Revision):
    def __init__(self, name, revision_datasources):
        # Initializes all of the Revision datasources
        super().__init__(name, revision_datasources)
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


class Diff(chars.Diff, edit_tokens.Diff, tokenized.Diff):
    pass
