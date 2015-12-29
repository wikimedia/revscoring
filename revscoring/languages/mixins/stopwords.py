from ...datasources import diff, parent_revision, revision
from ...datasources.meta import ItemMapper
from ...features.meta import ItemLength


class StopwordsSet:

    def __init__(self, *args, stopwords_set, **kwargs):
        self.stopwords_set = stopwords_set

        # Do the mixin!
        super(StopwordsSet, self).__init__(*args, **kwargs)

        # Datasources
        self.revision.stopword_tokens
        self.revision.non_stopword_tokens
        self.revision.content_stopword_tokens
        self.revision.content_non_stopword_tokens
        self.revision.stopword_token_frequency

        self.parent_revision.stopword_tokens
        self.parent_revision.non_stopword_tokens
        self.parent_revision.content_stopword_tokens
        self.parent_revision.content_non_stopword_tokens
        self.parent_revision.stopword_token_frequency

        self.diff.stopword_tokens_added
        self.diff.non_stopword_tokens_added
        self.diff.stopword_tokens_removed
        self.diff.non_stopword_tokens_removed
        self.diff.stopword_token_frequency_diff

        # Features
