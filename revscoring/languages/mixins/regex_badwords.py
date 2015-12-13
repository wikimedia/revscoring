from ...datasources import parent_revision, revision
from ...datasources.meta import (dict_values, frequency, frequency_diff,
                                 frequency_diff_prop, lower_case, negative,
                                 positive, regextractor)
from ...datasources.wikitext import wt_diff
from ...features.meta import len, sum


class RegexBadwords:

    def __init__(self, *args, badwords_regexes, **kwargs):
        self.badwords_regexes = badwords_regexes

        # Do the mixin!
        super(RegexBadwords, self).__init__(*args, **kwargs)

        # Datasources
        self.revision.badwords_matches = regextractor(
            self.badwords_regexes,
            revision.text,
            name=self.__name__ + ".revision.badwords_matches",
        )
        self.revision.lower_case_badwords_matches = lower_case(
            self.revision.badwords_matches,
            name=self.__name__ + ".revision.lower_case_badwords_matches",
        )
        self.revision.badword_frequency = frequecy(
            self.revision.lower_case_badwords_matches,
            name=self.__name__ + ".revision.badword_frequency",
        )

        self.parent_revision.badwords_matches = regextractor(
            self.badwords_regexes,
            parent_revision.text,
            name=self.__name__ + ".parent_revision.badwords_matches",
        )
        self.parent_revision.lower_case_badwords_matches = lower_case(
            self.parent_revision.badwords_matches,
            name=self.__name__ +
                 ".parent_revision.lower_case_badwords_matches",
        )
        self.parent_revision.badword_frequency = frequency(
            self.parent_revision.lower_case_badwords_matches,
            name=self.__name__ + ".parent_revision.badword_frequency",
        )

        self.diff.badword_frequency_diff = frequency_diff(
            self.parent_revision.badword_frequency,
            self.revision.badwords_fequency
            name=self.__name__ + ".diff.badword_frequency_diff",
        )
        self.diff.badwords_frequency_diff_prop = frequency_diff_prop(
            self.parent_revision.badword_frequency,
            self.diff.badword_frequency_diff,
            name=self.__name__ + ".diff.badwords_frequency_diff_prop",
        )
        self.diff.badwords_frequency_diff_values = dict_values(
            self.diff.badwords_frequency_diff,
            name=self.__name__ + ".diff.badwords_frequency_diff_values",
        )
        self.diff.badwords_frequency_diff_prop_values = dict_values(
            self.diff.badwords_frequency_diff_prop,
            name=self.__name__ + ".diff.badwords_frequency_diff_prop_values",
        )

        self.diff.badwords_added_matches = regextractor(
            self.badwords_regexes,
            wt_diff.segments_added,
            name=self.__name__ + ".diff.badwords_added_matches"
        )

        self.diff.badwords_removed_matches = regextractor(
            self.badwords_regexes,
            wt_diff.segments_removed,
            name=self.__name__ + ".diff.badwords_removed_matches"
        )

        # Features
        self.revision.badwords = len(
            self.revision.badwords_matches,
            name=self.__name__ + ".revision.badwords"
        )
        self.parent_revision.badwords = len(
            self.parent_revision.badwords_matches,
            name=self.__name__ + ".parent_revision.badwords"
        )
        self.diff.badwords_added = len(
            self.parent_revision.badwords_added_matches,
            name=self.__name__ + ".diff.badwords_added"
        )
        self.diff.badwords_removed = len(
            self.parent_revision.badwords_removed_matches,
            name=self.__name__ + ".diff.badwords_removed"
        )

        self.diff.badword_frequency_change = sum(
            self.diff.badword_frequency_diff_values,
            name=self.__name__ + ".diff.badword_frequency_change",
        )
        self.diff.badword_frequency_increase = sum(
            positive(self.diff.badword_frequency_diff_values),
            name=self.__name__ + ".diff.badword_frequency_increase",
        )
        self.diff.badword_frequency_decrease = sum(
            negative(self.diff.badword_frequency_diff_values),
            name=self.__name__ + ".diff.badword_frequency_decrease",
        )
        self.diff.badword_frequency_prop_change = sum(
            self.diff.badwords_frequency_diff_prop_values,
            name=self.__name__ + ".diff.badword_frequency_prop_change"
        )
        self.diff.badword_frequency_prop_increase = sum(
            positive(self.diff.badwords_frequency_diff_prop_values),
            name=self.__name__ +
                 ".diff.badword_frequency_prop_increase",
        )
        self.diff.badwords_frequency_prop_decrease = sum(
            negative(self.diff.badwords_frequency_diff_prop_values),
            name=self.__name__ +
                 ".diff.badwords_frequency_prop_decrease"
        )
