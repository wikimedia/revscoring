from ....datasources.meta import extractors, frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):

    def __init__(self, name, words, wikitext_revision):
        super().__init__(name)

        self.text = wikitext_revision.text

        self.matches = extractors.trie(
            words, self.text,
            name=name + ".matches",
        )

        self.match_frequency = frequencies.table(
            mappers.lower_case(self.matches),
            name=name + ".match_frequency",
        )

        if hasattr(wikitext_revision, 'parent'):
            self.parent = Revision(name + ".parent", words,
                                   wikitext_revision.parent)

        if hasattr(wikitext_revision, 'diff'):
            self.diff = Diff(name + ".diff", words,
                             wikitext_revision.diff, self)


class Diff(DependentSet):

    def __init__(self, name, words, wikitext_diff, revision):
        super().__init__(name)

        segments_added = wikitext_diff.segments_added
        segments_removed = wikitext_diff.segments_removed

        self.matches_added = extractors.trie(
            words, segments_added,
            name=name + ".matches_added")

        self.matches_removed = extractors.trie(
            words, segments_removed,
            name=name + ".matches_removed")

        self.match_delta = frequencies.delta(
            revision.parent.match_frequency,
            revision.match_frequency,
            name=name + ".match_delta"
        )
        self.match_prop_delta = frequencies.prop_delta(
            revision.parent.match_frequency,
            self.match_delta,
            name=name + ".match_prop_delta"
        )
