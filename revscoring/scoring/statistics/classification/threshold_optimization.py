import re


class ThresholdOptimization:
    STRING_PATTERN = re.compile(
        r"(maximum|minimum) "
        r"((!|[^\W\d])[\w]*) @ "  # target_stat
        r"((!|[^\W\d])[\w]*) "  # cond_stat
        r"(>=|<=) "  # greater
        r"([-+]?([0-9]*\.[0-9]+|[0-9]+))")  # cond_value

    def __init__(self, maximize, target_stat, cond_stat, greater, cond_value):
        """
        Construct a structured statement about an optimization metric.

        :Parameters:
            maximize : `bool`
                If True, maximize, else minimize
            target_stat : `str`
                The name of the target statistic that will be optimized
            cond_stat : `str`
                The name of the conditional statistic
            greater : `bool`
                The relationship between the conditional statistic and the
                conditional value.  If True, cond_stat >= cond_value, else
                cond_stat <= cond_value
            cond_value : `float`
                The conditional value
        """
        self.maximize = maximize
        self.target_stat = target_stat
        self.cond_stat = cond_stat
        self.greater = greater
        self.cond_value = cond_value

    def __str__(self):
        return "{0} {1} @ {2} {3} {4}" \
               .format("maximum" if self.maximize else "minimum",
                       self.target_stat,
                       self.cond_stat,
                       ">=" if self.greater else "<=",
                       self.cond_value)

    def repr(self):
        return "{0}.p({1!r})".format(self.__class__.__name__,
                                     str(self))

    def optimize_from(self, threshold_statistics):
        """
        Generates an optimized value by scanning a sequence of
        :class:`~revscoring.scoring.statistics.classification.ScaledThresholdStatistics`
        for a the best threshold that matches the conditional criteria. This
        function returns the value of the optimized target statistic (or None).
        """  # noqa
        val_tstats = self.get_optimal(threshold_statistics)
        if val_tstats is not None:
            return val_tstats[0]
        else:
            return None

    def get_optimal(self, threshold_statistics):
        """
        Generates an optimized value by scanning a sequence of
        :class:`~revscoring.scoring.statistics.classification.ScaledThresholdStatistics`
        for a the best threshold that matches the conditional criteria.  This
        function returns the entire
        :class:`~revscoring.scoring.statistics.classification.ScaledPredictionStatistics`
        mapping at the optimal threshold.
        """  # noqa
        if self.greater:
            filtered = [(tstats[self.target_stat], t, tstats)
                        for t, tstats in threshold_statistics
                        if tstats[self.cond_stat] is not None and
                        tstats[self.target_stat] is not None and
                        tstats[self.cond_stat] >= self.cond_value]
        else:
            filtered = [(tstats[self.target_stat], t, tstats)
                        for t, tstats in threshold_statistics
                        if tstats[self.cond_stat] is not None and
                        tstats[self.target_stat] is not None and
                        tstats[self.cond_stat] <= self.cond_value]

        if not filtered:
            return None

        if self.maximize:
            optimal = max(filtered)
            return optimal[1], optimal[2]
        else:
            optimal = min(filtered)
            return optimal[1], optimal[2]

    @classmethod
    def parse(cls, pattern):
        """
        Parse a formatted string representing a threshold optimization. E.g.
        'maximum recall @ precision >= 0.9' or
        'minimum match_rate @ recall >= 0.9'.

        :Parameters:
            pattern : `str`
                The optimization pattern to parse
        """
        match = cls.STRING_PATTERN.match(pattern.strip().lower())
        if match is None:
            raise ValueError('{0!r} does not match optimization pattern: '
                             .format(pattern) +
                             '"(maximum|minimum) <target> @ ' +
                             '<cond> (>=|<=) [float]"')
        maximize, target, _, cond, _, greater, cond_value, _ = match.groups()
        return cls(maximize == "maximum",
                   target, cond,
                   greater == ">=",
                   float(cond_value))

    @classmethod
    def from_string(cls, p):
        return cls.parse(p)

    @classmethod
    def p(cls, p):
        return cls.parse(p)
