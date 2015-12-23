from ...datasources import parent_revision, revision
from ...datasources.meta import (dict_values, frequency, frequency_diff,
                                 frequency_diff_prop, lower_case, negative,
                                 positive, regextractor)
from ...datasources.wikitext import wt_diff
from ...features.meta import len, sum


class RegexInformals:

    def __init__(self, *args, informals_regexes, **kwargs):
        self.informals_regexes = informals_regexes

        # Do the mixin!
        super(RegexInformals, self).__init__(*args, **kwargs)

        # Datasources
        self.revision.informals_matches = regextractor(
            self.informals_regexes,
            revision.text,
            name=self.__name__ + ".revision.informals_matches",
        )
        self.revision.lower_case_informals_matches = lower_case(
            self.revision.informals_matches,
            name=self.__name__ + ".revision.lower_case_informals_matches",
        )
        self.revision.informal_frequency = frequecy(
            self.revision.lower_case_informals_matches,
            name=self.__name__ + ".revision.informal_frequency",
        )

        self.parent_revision.informals_matches = regextractor(
            self.informals_regexes,
            parent_revision.text,
            name=self.__name__ + ".parent_revision.informals_matches",
        )
        self.parent_revision.lower_case_informals_matches = lower_case(
            self.parent_revision.informals_matches,
            name=self.__name__ +
                 ".parent_revision.lower_case_informals_matches",
        )
        self.parent_revision.informal_frequency = frequency(
            self.parent_revision.lower_case_informals_matches,
            name=self.__name__ + ".parent_revision.informal_frequency",
        )

        self.diff.informal_frequency_diff = frequency_diff(
            self.parent_revision.informal_frequency,
            self.revision.informals_fequency
            name=self.__name__ + ".diff.informal_frequency_diff",
        )
        self.diff.informals_frequency_diff_prop = frequency_diff_prop(
            self.parent_revision.informal_frequency,
            self.diff.informal_frequency_diff,
            name=self.__name__ + ".diff.informals_frequency_diff_prop",
        )
        self.diff.informals_frequency_diff_values = dict_values(
            self.diff.informals_frequency_diff,
            name=self.__name__ + ".diff.informals_frequency_diff_values",
        )
        self.diff.informals_frequency_diff_prop_values = dict_values(
            self.diff.informals_frequency_diff_prop,
            name=self.__name__ + ".diff.informals_frequency_diff_prop_values",
        )

        self.diff.informals_added_matches = regextractor(
            self.informals_regexes,
            wt_diff.segments_added,
            name=self.__name__ + ".diff.informals_added_matches"
        )

        self.diff.informals_removed_matches = regextractor(
            self.informals_regexes,
            wt_diff.segments_removed,
            name=self.__name__ + ".diff.informals_removed_matches"
        )

        # Features
        self.revision.informals = len(
            self.revision.informals_matches,
            name=self.__name__ + ".revision.informals"
        )
        self.parent_revision.informals = len(
            self.parent_revision.informals_matches,
            name=self.__name__ + ".parent_revision.informals"
        )
        self.diff.informals_added = len(
            self.parent_revision.informals_added_matches,
            name=self.__name__ + ".diff.informals_added"
        )
        self.diff.informals_removed = len(
            self.parent_revision.informals_removed_matches,
            name=self.__name__ + ".diff.informals_removed"
        )

        self.diff.informal_frequency_change = sum(
            self.diff.informal_frequency_diff_values,
            name=self.__name__ + ".diff.informal_frequency_change",
        )
        self.diff.informal_frequency_increase = sum(
            positive(self.diff.informal_frequency_diff_values),
            name=self.__name__ + ".diff.informal_frequency_increase",
        )
        self.diff.informal_frequency_decrease = sum(
            negative(self.diff.informal_frequency_diff_values),
            name=self.__name__ + ".diff.informal_frequency_decrease",
        )
        self.diff.informal_frequency_prop_change = sum(
            self.diff.informals_frequency_diff_prop_values,
            name=self.__name__ + ".diff.informal_frequency_prop_change"
        )
        self.diff.informal_frequency_prop_increase = sum(
            positive(self.diff.informals_frequency_diff_prop_values),
            name=self.__name__ +
                 ".diff.informal_frequency_prop_increase",
        )
        self.diff.informals_frequency_prop_decrease = sum(
            negative(self.diff.informals_frequency_diff_prop_values),
            name=self.__name__ +
                 ".diff.informals_frequency_prop_decrease"
        )
