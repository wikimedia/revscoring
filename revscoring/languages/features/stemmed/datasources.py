from ....datasources.meta import frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):
    def __init__(self, name, stem_word, wikitext_revision):
        super().__init__(name)

        self.stems = mappers.map(
            stem_word, wikitext_revision.words,
            name=name + ".stems"
        )

        self.stem_frequency = frequencies.table(
            self.stems,
            name=name + ".stem_frequency"
        )

        if hasattr(wikitext_revision, 'parent'):
            self.parent = Revision(name + ".parent", stem_word,
                                   wikitext_revision.parent)

        if hasattr(wikitext_revision, 'diff'):
            self.diff = Diff(name + ".diff", stem_word,
                             wikitext_revision.diff, self)


class Diff(DependentSet):
    def __init__(self, name, stem_word, wikitext_diff, revision):
        super().__init__(name)

        self.stems_added = mappers.map(
            stem_word, wikitext_diff.words_added,
            name=name + ".stems_added"
        )
        self.stems_removed = mappers.map(
            stem_word, wikitext_diff.words_removed,
            name=name + ".stems_removed"
        )

        self.stem_delta = frequencies.delta(
            revision.parent.stem_frequency,
            revision.stem_frequency,
            name=name + ".stem_delta"
        )
        self.stem_prop_delta = frequencies.prop_delta(
            revision.parent.stem_frequency, self.stem_delta,
            name=name + ".stem_prop_delta"
        )
