from . import edit, parsed, sentences, tokenized
from ....dependencies import DependentSet


class BaseRevision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.text = revision_datasources.text

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )


class Revision(parsed.Revision, sentences.Revision, tokenized.Revision,
               BaseRevision):

    def __init__(self, name, revision_datasources):
        # Initializes all of the Revision datasources
        super().__init__(name, revision_datasources)

        # Initializes the diff using the Revision datasources
        if hasattr(revision_datasources, "diff"):
            self.diff = Diff(name + ".diff", self)


class BaseDiff(DependentSet):

    def __init__(self, name, revision):
        super().__init__(name)
        self.revision = revision


class Diff(edit.Diff, sentences.Diff, tokenized.Diff, BaseDiff):
    pass
