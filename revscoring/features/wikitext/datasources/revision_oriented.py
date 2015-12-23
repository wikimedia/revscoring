from . import edit, parsed, tokenized


class BaseRevision:

    def __init__(self, prefix, revision_datasources):
        self.prefix = prefix
        self.text = revision_datasources.text

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                prefix + ".parent",
                revision_datasources.parent
            )


class Revision(parsed.Revision, tokenized.Revision, BaseRevision):

    def __init__(self, prefix, revision_datasources):
        # Initializes all of the Revision datasources
        super().__init__(prefix, revision_datasources)

        # Initializes the diff using the Revision datasources
        if hasattr(revision_datasources, "diff"):
            self.diff = Diff(prefix + ".diff", self)


class BaseDiff:

    def __init__(self, prefix, revision):
        self.prefix = prefix
        self.revision = revision


class Diff(edit.Diff, tokenized.Diff, BaseDiff):
    pass
