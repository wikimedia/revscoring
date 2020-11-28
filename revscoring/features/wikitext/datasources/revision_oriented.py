from . import edit, parsed, sentences, tokenized


class Revision(parsed.Revision, sentences.Revision, tokenized.Revision):
    # pass
    def __init__(self, name, revision_datasources):
        # Initializes all of the Revision datasources
        super().__init__(name, revision_datasources)

        # Initializes the diff using the Revision datasources
        if hasattr(revision_datasources, "diff"):
            self.diff = Diff(name + ".diff", self)


class Diff(edit.Diff, sentences.Diff, tokenized.Diff):
    pass
