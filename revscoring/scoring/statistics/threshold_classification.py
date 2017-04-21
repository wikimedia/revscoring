import logging
import re

import tabulate
from numpy import all, diff, interp, linspace
from sklearn.metrics import auc

from . import util
from .classification import Classification, LabelStatistics, MicroMacroStat

logger = logging.getLogger(__name__)


class ThresholdClassification(Classification):
    FIELDS = ['roc_auc', 'pr_auc', 'thresholds']

    def __init__(self, *args, decision_key="probability", max_thresholds=200,
                 threshold_optimizations=None, **kwargs):
        """
        :Parameters:
            population_rates : `dict`
                A mapping of label classes with float representing the rate
                that each class occurs in the target population.  Rates
                observed in the sample will be scaled to match the population
                rates.
            max_thresholds : `int`
                The maximum number of thresholds to report.  Thresholds will
                be distributed uniformly across actually output probabilities.
        """
        super().__init__(*args, **kwargs)
        self.decision_key = decision_key
        self.max_thresholds = max_thresholds
        self.threshold_optimizations = {
            str(to): to for to in (threshold_optimizations or [])}

    def fit(self, score_labels):
        super().fit(score_labels)

        threshold_stats = {}
        for label in self.labels:
            threshold_stats[label] = ThresholdStatistics(
                [s[self.decision_key][label] for s, l in score_labels],
                [l == label for s, l in score_labels],
                population_rate=self.population_rates.get(label),
                threshold_optimizations=self.threshold_optimizations)

        for stat_name in ThresholdStatistics.FIELDS:
            self[stat_name] = MicroMacroStat(stat_name, threshold_stats)

        for op_name in self.threshold_optimizations:
            self[op_name] = MicroMacroStat(op_name, threshold_stats)

        self['thresholds'] = {
            label: ThresholdStatList(tstats, self.max_thresholds)
            for label, tstats in threshold_stats.items()}

    def format_str(self, fields=None, ndigits=3):
        fields = fields or (Classification.FIELDS +
                            list(self.threshold_optimizations.keys()) +
                            ThresholdClassification.FIELDS)
        formatted = super().format_str(fields=fields, ndigits=ndigits)
        for field in fields:
            if field == "thresholds":
                formatted += "thresholds:\n"
                for label in self.labels:
                    formatted += util.tab_it_in(repr(label))
                    table_str = self['thresholds'][label] \
                                .format_str(ndigits=ndigits)
                    formatted += util.tab_it_in(table_str, 2)
                formatted += "\n"
            elif field in ThresholdClassification.FIELDS or \
                 field in self.threshold_optimizations:
                formatted += self[field].format_str(
                    self.labels, ndigits=ndigits)
                formatted += "\n"
        return formatted

    def format_json(self, fields=None, ndigits=3):
        fields = fields or (Classification.FIELDS +
                            ThresholdClassification.FIELDS +
                            list(self.threshold_optimizations.keys()))
        stats_doc = super().format_json(fields=fields, ndigits=ndigits)

        for field in fields:
            if field == "thresholds":
                stats_doc['thresholds'] = {
                    label: ltstats.format_json(ndigits=ndigits)
                    for label, ltstats in self['thresholds'].items()}
            elif field in ThresholdClassification.FIELDS:
                stats_doc[field] = self[field].format_json(ndigits=ndigits)

        return stats_doc


class ThresholdOptimization(dict):
    STRING_PATTERN = re.compile(
        r"(maximum|minimum) "
        r"([^\W\d][\w]*) @ "  # target_stat
        r"([^\W\d][\w]*) "  # cond_stat
        r"(>=|<=) "  # greater
        r"([-+]?([0-9]*\.[0-9]+|[0-9]+))")  # cond_value

    def __init__(self, maximize, target_stat, cond_stat, greater, cond_value):
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

    def optimize_from(self, threshold_statistics):
        if self.greater:
            filtered = [(lstats.get_stat(self.target_stat), t, lstats)
                        for t, lstats in threshold_statistics
                        if lstats.get_stat(self.cond_stat) >= self.cond_value]
        else:
            filtered = [(lstats.get_stat(self.target_stat), t, lstats)
                        for t, lstats in threshold_statistics
                        if lstats.get_stat(self.cond_stat) <= self.cond_value]

        if not filtered:
            return None

        if self.maximize:
            return max(filtered)[0]
        else:
            return min(filtered)[0]

    @classmethod
    def from_string(cls, string):
        match = cls.STRING_PATTERN.match(string.strip().lower())
        if match is None:
            raise ValueError('{0!r} does not match optimization pattern: '
                             .format(string) +
                             '"(maximum|minimum) <target> @ ' +
                             '<cond> (>=|<=) [float]"')
        maximize, target, cond, greater, cond_value, _ = match.groups()
        return cls(maximize == "maximum",
                   target, cond,
                   greater == ">=",
                   float(cond_value))


class ThresholdStatistics(list):
    FIELDS = ['roc_auc', 'pr_auc']

    def __init__(self, y_decisions, y_trues, population_rate=None,
                 threshold_optimizations=None):
        super().__init__()
        if population_rate is None:
            self.trues = sum(y_trues)
        else:
            n_true = sum(y_trues)
            observed_rate = n_true / len(y_trues)
            self.trues = sum(y_trues) * (population_rate / observed_rate)
        self.threshold_optimizations = threshold_optimizations or {}
        unique_thresholds = sorted(set(y_decisions))

        for threshold in unique_thresholds:
            self.append((threshold, LabelStatistics(
                [decision >= threshold for decision in y_decisions],
                 y_trues, population_rate=population_rate))
            )

    def roc_auc(self):
        return zero_to_one_auc([stat.fpr() for t, stat in self],
                               [stat.recall() for t, stat in self])

    def pr_auc(self):
        return zero_to_one_auc([stat.recall() for t, stat in self],
                               [stat.precision() for t, stat in self])

    def get_stat(self, stat_name):
        if not hasattr(self, stat_name):
            if stat_name in self.threshold_optimizations:
                optimization = self.threshold_optimizations[stat_name]
                return optimization.optimize_from(self)
            else:
                raise KeyError(stat_name)
        else:
            return getattr(self, stat_name)()

    def best(self, stat_name, at_value):
        for threshold, lstats in self:
            target_stat = lstats.get_stat(stat_name)
            if target_stat >= at_value:
                return threshold, lstats

    def optimize(self, optimize, stat_name, at_value):
        best_threshold = self.best(stat_name, at_value)
        if best_threshold is None:
            return None
        else:
            threshold, lstats = best_threshold
            return lstats.get_stat(stat_name)


def zero_to_one_auc(x_vals, y_vals):
    x_space = linspace(0, 1, 50)
    if all(diff(x_vals) > 0):
        y_interp = interp(x_space, x_vals, y_vals)
    else:
        y_interp = interp(
            x_space, list(reversed(x_vals)), list(reversed(y_vals)))
    return auc(x_space, y_interp)


class ThresholdStatList(list):

    def __init__(self, threshold_stats, max_thresholds):
        if max_thresholds is None or len(threshold_stats) < max_thresholds:
            limited_threshold_stats = threshold_stats
        else:
            step = len(threshold_stats) / max_thresholds
            float_i = 0
            limited_threshold_stats = []
            while float_i <= len(threshold_stats) - 2:
                limited_threshold_stats.append(threshold_stats[int(float_i)])
                float_i += step
            limited_threshold_stats.append(threshold_stats[-1])

        super().__init__(limited_threshold_stats)

    def format_str(self, fields=None, ndigits=3):
        fields = fields or LabelStatistics.FIELDS
        table_data = [[util.round(threshold, ndigits + 2)] +
                      [util.round(tstats.get_stat(field), ndigits)
                       for field in fields]
                      for threshold, tstats in self]
        headers = ['threshold'] + fields
        return tabulate.tabulate(table_data, headers=headers)

    def format_json(self, fields=None, ndigits=3):
        thresholds_doc = []
        for threshold, tstats in self:
            tstats_doc = tstats.format_json(fields, ndigits=3)
            tstats_doc['threshold'] = threshold
            thresholds_doc.append(tstats_doc)
        return thresholds_doc
