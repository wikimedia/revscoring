import logging
from collections import OrderedDict

from ... import util
from ..statistics import Statistics
from .counts import Counts
from .micro_macro_stats import MicroMacroStats
from .rates import Rates
from .scaled_prediction_statistics import ScaledPredictionStatistics
from .scaled_threshold_statistics import ScaledThresholdStatistics
from .threshold_optimization import ThresholdOptimization

logger = logging.getLogger(__name__)


class Classification(Statistics):

    def __init__(self, prediction_key="prediction", decision_key=None,
                 labels=None, population_rates=None, **kwargs):
        """
        Constructs a set of classification statistics

        :Parameters:
            prediction_key : `str`
                A key into a score doc under which a class predition value
                can be found
            decision_key : `str`
                A key into a score doc under which a scalar decision value
                can be found for each potential class.
            labels : [ `mixed` ]
                A sequence of labels that are in-order.  Order is used when
                formatting statistical outputs.
            population_rates : `dict`
                A mapping of label classes with float representing the rate
                that each class occurs in the target population.  Rates
                observed in the sample will be scaled to match the population
                rates.  This is useful when training a model with different
                sample rates than the target population rates.
        """
        super().__init__()
        self.prediction_key = prediction_key
        self.decision_key = decision_key
        self.labels = labels
        self.population_rates = population_rates or {}

    def fit(self, score_labels):
        """
        Fit to scores and labels.

        :Parameters:
            score_labels : [( `dict`, `mixed` )]
                A collection of scores-label pairs generated using
                :class:`revscoring.Model.score`.  Note that fitting is usually
                done using data withheld during model training
        """
        super().fit(score_labels)
        if self.labels is None:
            self.labels = sorted(set(l for s, l in score_labels))

        self['counts'] = Counts(self.labels, score_labels, self.prediction_key)
        self['rates'] = Rates(self['counts'],
                              population_rates=self.population_rates)

        self.label_stats = OrderedDict()
        for label in self.labels:
            self.label_stats[label] = ScaledPredictionStatistics(
                y_preds=[s[self.prediction_key] == label
                         for s, l in score_labels],
                y_trues=[l == label for s, l in score_labels],
                population_rate=self.population_rates.get(label))

        self['match_rate'] = \
            MicroMacroStats(self.label_stats, 'match_rate')
        self['filter_rate'] = \
            MicroMacroStats(self.label_stats, 'filter_rate')
        self['recall'] = \
            MicroMacroStats(self.label_stats, 'recall')
        self['!recall'] = \
            MicroMacroStats(self.label_stats, '!recall')
        self['precision'] = \
            MicroMacroStats(self.label_stats, 'precision')
        self['!precision'] = \
            MicroMacroStats(self.label_stats, '!precision')
        self['f1'] = \
            MicroMacroStats(self.label_stats, 'f1')
        self['!f1'] = \
            MicroMacroStats(self.label_stats, '!f1')
        self['accuracy'] = \
            MicroMacroStats(self.label_stats, 'accuracy')
        self['fpr'] = \
            MicroMacroStats(self.label_stats, 'fpr')

        if self.decision_key is not None:
            self.label_thresholds = OrderedDict()
            for label in self.labels:
                self.label_thresholds[label] = ScaledThresholdStatistics(
                    [s[self.decision_key][label] for s, l in score_labels],
                    [l == label for s, l in score_labels],
                    population_rate=self.population_rates.get(label))

            self['roc_auc'] = \
                MicroMacroStats(self.label_thresholds, 'roc_auc')
            self['pr_auc'] = \
                MicroMacroStats(self.label_thresholds, 'pr_auc')

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        elif hasattr(self, "label_thresholds"):
            #  This handles the case where a 'key' is a threshold optimization
            try:
                optimization = ThresholdOptimization.parse(key)
            except ValueError:
                raise KeyError(
                    ("{0} not found, and does not match pattern " +
                     "for threshold optimizations: {1}").format(
                        key, ThresholdOptimization.STRING_PATTERN.pattern))
            return MicroMacroStats(self.label_thresholds, optimization)
        else:
            raise KeyError(key)

    def lookup(self, path):
        if isinstance(path, str):
            path = util.parse_pattern(path)
        key = path[0]
        return self[key].lookup(path[1:])

    def format_str(self, path_tree, **kwargs):
        """
        Formats path tree into a table and rounding to at most `ndigits`.
        """
        formatted = "Statistics:\n"

        for key in path_tree or self.keys():
            sub_tree = path_tree.get(key, {})
            formatted += self[key].format_str(sub_tree, **kwargs)

        return formatted

    def format_json(self, path_tree, **kwargs):
        """
        Formats a json-able dictionary including rounding to
        at most `ndigits`.
        """
        doc = OrderedDict()

        for key in path_tree.keys() or self.keys():
            sub_tree = path_tree.get(key, {})
            doc[key] = self[key].format_json(sub_tree, **kwargs)

        return doc
