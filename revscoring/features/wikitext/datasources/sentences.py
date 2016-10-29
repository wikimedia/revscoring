from deltas.segmenters import MatchableSegment

from ....datasources import Datasource
from ....datasources.meta import indexable


class Revision:

    def __init__(self, name, revision_datasources):
        super().__init__(name, revision_datasources)

        self.sentences = Datasource(
            self._name + ".sentences", psw2sentences,
            depends_on=[self.paragraphs_sentences_and_whitespace]
        )
        """
        A list of "sentences" extracted from the text.
        """


class Diff():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sentences_added_removed = Datasource(
            self._name + ".sentences_added_removed", set_diff,
            depends_on=[self.revision.sentences,
                        self.revision.parent.sentences]
        )

        self.sentences_added = indexable.index(
            0, self.sentences_added_removed,
            name=self._name + ".sentences_added"
        )
        """
        A set of sentences that were added in this edit
        """

        self.sentences_removed = indexable.index(
            1, self.sentences_added_removed,
            name=self._name + ".sentences_removed"
        )
        """
        A set of sentences that were removed in this edit
        """


def psw2sentences(segments):
    sentences = []
    for paragraph_or_whitespace in segments:
        if isinstance(paragraph_or_whitespace, MatchableSegment):
            paragraph = paragraph_or_whitespace  # We have a paragraph
            for sentence_or_whitespace in paragraph:
                if isinstance(sentence_or_whitespace, MatchableSegment):
                    sentence = sentence_or_whitespace  # We have a sentence
                    sentences.append(sentence)
    return sentences


def set_diff(a, b):
    a, b = set(a), set(b)
    return (a - b, b - a)
