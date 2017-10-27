import logging

logger = logging.getLogger(__name__)


class ScaledClassificationMatrix:

    __slots__ = ('tp', 'fp', 'tn', 'fn',
                 'n', 'positives', 'negatives',
                 'trues', 'falses', 'correct',
                 'population_rate')

    def __init__(self, y_preds=None, y_trues=None,
                 counts=None, population_rate=None):
        """
        Constructs a classification matrix and scales the values based on a
        population rate.

        :Parameters:
            y_preds : [ `bool` ]
                Predictions where `True` represents a prediction of the target
                class
            y_trues : [ `bool` ]
                Labels where `True` represents a label matching the target
                class
            counts : ( `int`, `int`, `int`, `int` )
                A tuple of tp, fp, tn, fn
            population_rate : `float`
                The rate at which this label occurs in the population.  If
                not provided, the sample rate will be assumed to reflect the
                population rate.
        """
        self.population_rate = population_rate
        if counts is None:
            self.fit(y_preds, y_trues)
        else:
            self.rescale(*counts)

    @classmethod
    def fit_counts(cls, y_preds, y_trues):
        # Generate counts of basic classification metrics
        tp, fp, tn, fn = 0, 0, 0, 0
        for y_pred, y in zip(y_preds, y_trues):
            tp += y_pred and y  # win
            fn += not y_pred and y  # fail
            tn += not y_pred and not y  # win
            fp += y_pred and not y  # fail

        return (tp, fp, tn, fn)

    def fit(self, y_preds, y_trues):
        """
        :Parameters:
            y_preds : [ `bool` ]
                Predictions where `True` represents a prediction of the target
                class
            y_trues : [ `bool` ]
                Labels where `True` represents a label matching the target
                class
        """
        counts = self.fit_counts(y_preds, y_trues)
        self.rescale(*counts)

    def rescale(self, tp, fp, tn, fn):
        """
        Re-scale a matrix based on sample counts

        :Parameters:
            tp : int
                True positives
            fp : int
                False positives
            tn : int
                True negatives
            fn : int
                False negatives

        """
        self.tp, self.fp, self.tn, self.fn = tp, fp, tn, fn
        if self.population_rate is not None:
            observed_rate = ((self.tp + self.fn) /
                             (self.tp + self.fn + self.tn + self.fp))
            sample_rate = observed_rate / self.population_rate
            non_sample_rate = (1 - observed_rate) / (1 - self.population_rate)

            # Apply scaling to obtain expected population rate
            self.tp = self.tp / sample_rate
            self.fn = self.fn / sample_rate
            self.tn = self.tn / non_sample_rate
            self.fp = self.fp / non_sample_rate

        # Useful variables
        self.n = self.tp + self.tn + \
            self.fp + self.fn
        self.positives = self.tp + self.fp
        self.negatives = self.tn + self.fn
        self.trues = self.tp + self.fn
        self.falses = self.fp + self.tn
        self.correct = self.tp + self.tn
