from . import chars, edit_tokens, parsed, tokenized

prefix = "wikitext.revision"


class BaseRevision:

    def __init__(self, prefix, revision_datasources):
        self.prefix = prefix
        self.datasources = revision_datasources

        if hasattr(self.datasources, "parent"):
            self.parent = Revision(
                prefix + ".parent",
                self.datasources.parent
            )

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(
                prefix + ".diff",
                self.datasources.diff
            )


class Revision(parsed.Revision, chars.Revision, tokenized.Revision,
               BaseRevision):
    pass


class BaseDiff:

    def __init__(self, prefix, diff_datasources):
        self.prefix = prefix
        self.datasources = diff_datasources


class Diff(chars.Diff, edit_tokens.Diff, tokenized.Diff, BaseDiff):
    pass
