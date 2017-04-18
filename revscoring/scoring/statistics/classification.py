import logging
from collections import defaultdict

import tabulate

from . import util
from .statistics import Statistics

logger = logging.getLogger(__name__)


class Classification(Statistics):
    FIELDS = ['counts', 'rates', 'filter_rate', 'precision', 'recall',
              'accuracy', 'f1']

    def __init__(self, *args, prediction_key="prediction",
                 labels=None, population_rates=None, **kwargs):
        super().__init__()
        self.prediction_key = prediction_key
        self.labels = labels
        self.population_rates = population_rates or {}

    def fit(self, score_labels):
        super().fit(score_labels)
        if self.labels is None:
            self.labels = sorted(set(l for s, l in score_labels))

        y_preds = [s[self.prediction_key] for s, l in score_labels]
        label_stats = {}
        for label in self.labels:
            label_stats[label] = LabelStatistics(
                [y_pred == label for y_pred in y_preds],
                [l == label for s, l in score_labels],
                population_rate=self.population_rates.get(label))

        self['counts'] = Counts(score_labels)
        self['rates'] = Rates(self['counts'],
                              population_rates=self.population_rates)

        for stat_name in Classification.FIELDS:
            if stat_name in {'counts', 'rates'}:
                continue
            self[stat_name] = MicroMacroStat(stat_name, label_stats)

    def format_str(self, fields=None, ndigits=3):
        """
        Formats `fields` into a table and rounding to at most `ndigits`.
        """
        fields = fields or Classification.FIELDS
        formatted = ""

        for field in fields:
            if field == 'counts':
                formatted += self['counts'].format_str(self.labels)
                formatted += "\n"
            elif field == 'rates':
                formatted += self['rates'].format_str(
                    self.labels, ndigits=ndigits)
                formatted += "\n"
            elif field in Classification.FIELDS:
                formatted += self[field].format_str(
                    self.labels, ndigits=ndigits)
                formatted += "\n"

        return formatted

    def format_json(self, fields=None, ndigits=3):
        """
        Formats a json-able dictionary including `fields` and rounding to
        at most `ndigits`.
        """
        fields = fields or Classification.FIELDS
        stats_doc = {}
        for field in fields:
            if field == 'counts':
                stats_doc['counts'] = self['counts'].format_json()
            elif field == 'rates':
                stats_doc['rates'] = self['rates'].format_json(ndigits=ndigits)
            elif field in Classification.FIELDS:
                stats_doc[field] = self[field].format_json(ndigits=ndigits)
        return stats_doc


class MicroMacroStat(dict):

    def __init__(self, stat_name, label_stats):
        self.stat_name = stat_name
        self['micro'] = (
                sum(lstats.get_stat(stat_name) * lstats.n
                    for lstats in label_stats.values()) /
                sum(lstats.n for lstats in label_stats.values()))
        self['macro'] = (
                sum(lstats.get_stat(stat_name)
                    for lstats in label_stats.values()) /
                len(label_stats))
        self['labels'] = {label: lstats.get_stat(stat_name)
                          for label, lstats in label_stats.items()}

    def format_str(self, labels, ndigits=3):
        formatted = "{0} (micro={1}, macro={2}):\n" \
                     .format(self.stat_name,
                             util.round(self['micro'], ndigits=ndigits),
                             util.round(self['macro'], ndigits=ndigits))
        table_str = tabulate.tabulate(
            [[util.round(self['labels'][l], ndigits) for l in labels]],
            headers=labels)
        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self, ndigits=3):
        return {
            'micro': util.round(self['micro'], ndigits),
            'macro': util.round(self['micro'], ndigits),
            'labels': {l: util.round(self['labels'][l], ndigits)
                       for l in self['labels']}
        }


class ScaledClassificationMatrix:

    def __init__(self, y_preds, y_trues, population_rate=None):
        """
        Constructs a classification matrix and scales the values based on a
        population rate.
        """
        self.population_rate = population_rate

        # Generate counts of basic classification metrics
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0
        for y_pred, y in zip(y_preds, y_trues):
            self.tp += y_pred and y  # win
            self.fn += not y_pred and y  # fail
            self.tn += not y_pred and not y  # win
            self.fp += y_pred and not y  # fail

        if population_rate is not None:
            observed_rate = ((self.tp + self.fn) /
                             (self.tp + self.fn + self.tn + self.fp))
            sample_rate = observed_rate / population_rate
            non_sample_rate = (1 - observed_rate) / (1 - population_rate)

            # Apply scaling to obtain expected population rate
            self.tp = self.tp / sample_rate
            self.fn = self.fn / sample_rate
            self.tn = self.tn / non_sample_rate
            self.fp = self.fp / non_sample_rate
            '''
            orig_tp = self.tp
            orig_fn = self.fn
            orig_tn = self.tn
            orig_fp = self.fp
            logger.debug("Scaled true-positives ({0}) by sample_rate {1}: {2}"
                         .format(orig_tp, sample_rate, self.tp))
            logger.debug("Scaled false-negatives ({0}) by sample_rate {1}: {2}"
                         .format(orig_fn, sample_rate, self.fn))
            logger.debug("Scaled true-negatives ({0}) by sample_rate {1}: {2}"
                         .format(orig_tn, sample_rate, self.tn))
            logger.debug("Scaled false-positives ({0}) by sample_rate {1}: {2}"
                         .format(orig_fp, sample_rate, self.fp))
            '''

        # Useful variables
        self.n = self.tp + self.tn + \
                 self.fp + self.fn
        self.positives = self.tp + self.fp
        self.negatives = self.tn + self.fn
        self.trues = self.tp + self.fn
        self.falses = self.fp + self.tn
        self.correct = self.tp + self.tn


class LabelStatistics(ScaledClassificationMatrix):
    FIELDS = ['match_rate', 'filter_rate',
              'precision', '!precision',
              'recall', '!recall',
              'accuracy', 'fpr',
              'f1', '!f1']

    def __init__(self, y_pred, y_trues, population_rate=None):
        """
        Constructs a basic set of statistics about a classification matrix.

        :Parameters:
            y_pred : `iterable` ( `bool` )
                A sequence of predictions where `True` represents a matched
                observation for a specific label.
            y_trues : `iterable` ( `bool` )
                A sequence of labels where `True` represents a positive
                observation.
            population_rate : `float`
                The rate at which the observed class appears in the population.
                This value will be used to re-scale the number of y_trues
                across all metrics.
        """
        super().__init__(y_pred, y_trues, population_rate=population_rate)

    def format(self, *args, formatting="str", **kwargs):
        if formatting == "str":
            return self.format_str(*args, **kwargs)
        elif formatting == "json":
            return self.format_json(*args, **kwargs)
        else:
            raise ValueError("Unknown formatting {0!r}".format(formatting))

    def format_json(self, fields=None, ndigits=3):
        fields = fields or self.FIELDS
        return {f: util.round(self.get_stat(f), ndigits)
                for f in fields}

    def format_str(self, fields=None, ndigits=3):
        fields = fields or self.FIELDS
        table_data = [[util.round(self.get_stat(f), ndigits) for f in fields]]
        return tabulate.tabulate(table_data, headers=fields)

    def get_stat(self, stat_name):
        method_name = stat_name.replace("!", "_")

        if not hasattr(self, method_name):
            raise KeyError(stat_name)
        else:
            return getattr(self, method_name)()

    def match_rate(self):
        """
        The proportion of observations that are matched in prediction.

            match-rate = positives / n
        """
        return (self.positives / self.n) if self.n is not 0 else None

    def filter_rate(self):
        """
        The proportion of observations that are not matched.

            filter-rate = 1 - match-rate
        """
        return (1 - self.match_rate()) \
               if self.match_rate() is not None else None

    def accuracy(self):
        """
        The proportion of predictions that were right.

            accuracy = correct / n
        """
        return (self.correct / self.n) if self.n != 0 else None

    def recall(self):
        """
        The proportion of the target class that the classifier matches.
        AKA "true-positive rate" and "sensitivity".

            recall = true-positives / target-class
        """
        return (self.tp / self.trues) if self.trues != 0 else None

    def _recall(self):
        """
        The inverse recall.  The proportion of non-target class items that are
        not matched.

            !recall = true-negatives / !target-class
        """
        return (self.tn / self.falses) if self.falses != 0 else None

    def fpr(self):
        """
        False-positive rate.  The proportion of proportion of non-target class
        items that are not matched.

            fpr = false-positives / !target-class
        """
        return (self.fp / self.falses) if self.falses != 0 else None

    def precision(self):
        """
        The proportion of matched observations that are correctly matched.
        AKA "positive predictive value".

            precision = true-positives / true-predicions
        """
        return (self.tp / self.positives) if self.positives != 0 else None

    def _precision(self):
        """
        The proportion of non-matched observations that are correctly not
        matched.  AKA "negative predictive value"

            !precision = true-negatives / false-predictions
        """
        return (self.tn / self.negatives) if self.negatives != 0 else None

    def f1(self):
        """
        An information theoretic statistic that balances specificity with
        sensitivity.
        """
        return (2 * ((self.precision() * self.recall()) /
                     (self.precision() + self.recall()))
                if self.precision() is not None and
                   self.recall() is not None and
                   self.precision() + self.recall() > 0 else None)

    def _f1(self):
        """
        The inverse f1.  The same information theoretic statistic applied to
        non-matched observations.
        """
        return (2 * ((self._precision() * self._recall()) /
                     (self._precision() + self._recall()))
                if self._precision() is not None and
                   self._recall() is not None and
                   self._precision() + self._recall() > 0 else None)


class Counts(dict):

    def __init__(self, score_labels):
        super().__init__()
        self['n'] = len(score_labels)

        self['labels'] = defaultdict(int)
        predictions = defaultdict(lambda: defaultdict(int))

        for score, label in score_labels:
            self['labels'][label] += 1
            predictions[label][score['prediction']] += 1

        self['predictions'] = {label: dict(pred)
                               for label, pred in predictions.items()}

    def format_str(self, labels):
        formatted = "counts (n={0}):\n".format(self['n'])
        table_data = [
            [repr(label), self['labels'][label], '-->'] +
            [self['predictions'].get(label, {}).get(pred, 0)
             for pred in labels]
            for label in labels]
        table_str = tabulate.tabulate(
            table_data, headers=['label', 'n', ''] +
                                ["~{0}".format(l) for l in labels])
        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self):
        return self


class Rates(dict):

    def __init__(self, counts, population_rates=None):
        self['sample'] = {label: lcount / counts['n']
                          for label, lcount in counts['labels'].items()}
        if population_rates:
            self['population'] = population_rates

    def format_str(self, labels, ndigits=3):
        formatted = "rates:\n"
        table_data = [
            [group] + [util.round(self[group][label], ndigits)
                       for label in labels]
            for group in self]

        table_str = tabulate.tabulate(
            table_data, headers=[''] + [repr(l) for l in labels])
        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self, ndigits=3):
        return {group: {label: util.round(rate)
                        for label, rate in lrates.items()}
                for group, lrates in self.items()}
