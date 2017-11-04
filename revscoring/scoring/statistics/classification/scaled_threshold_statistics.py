from itertools import groupby

from numpy import all, diff, interp, isnan, linspace
from sklearn.metrics import auc
from tabulate import tabulate

from ... import util
from .scaled_prediction_statistics import ScaledPredictionStatistics
from .threshold_optimization import ThresholdOptimization


class ScaledThresholdStatistics(list):
    FIELDS = ['roc_auc', 'pr_auc']

    def __init__(self, y_decisions, y_trues, population_rate=None,
                 threshold_ndigits=None):
        """
        Construct a sequence of ThresholdStatistics

        :Parameters:
            y_decisions : [ `float` ]
                A sequence of decision-weights that represent confidence in
                a target class prediction
            y_trues : [ `bool` ]
                A sequence of labels where `True` represents a positive
                observation.
            population_rate : `float`
                The rate at which the observed class appears in the population.
                This value will be used to re-scale the number of y_trues
                across all metrics.
            threshold_ndigits : `int`
                If set, round the threshold by this many decimals to compress
                threshold statistics information.
        """  # noqa
        super().__init__()
        if population_rate is None:
            self.trues = sum(y_trues)
        else:
            n_true = sum(y_trues)
            observed_rate = n_true / len(y_trues)
            self.trues = sum(y_trues) * (population_rate / observed_rate)

        if threshold_ndigits is not None:
            y_decisions = [util.round(d, threshold_ndigits)
                           for d in y_decisions]
        threshold_groups = groupby(
            sorted((y_d, y_t) for y_d, y_t in zip(y_decisions, y_trues)),
            key=lambda p: p[0])

        tp, fp, tn, fn = sum(y_trues), sum(not t for t in y_trues), 0, 0
        for threshold, group in threshold_groups:
            sps = ScaledPredictionStatistics(
                counts=(tp, fp, tn, fn), population_rate=population_rate)
            self.append((threshold, sps))
            for _, y_true in group:
                tp -= y_true
                fp -= not y_true
                tn += not y_true
                fn += y_true

    def roc_auc(self):
        return zero_to_one_auc([stat.fpr() for t, stat in self],
                               [stat.recall() for t, stat in self])

    def pr_auc(self):
        return zero_to_one_auc(
            [stat.recall() for t, stat in self
             if None not in (stat.recall(), stat.precision())],
            [stat.precision() for t, stat in self
             if None not in (stat.recall(), stat.precision())])

    def __getitem__(self, field):
        if field in self.FIELDS:
            method_name = field.replace("!", "_")
            return getattr(self, method_name)()
        elif isinstance(field, int):
            return super.__getitem__(field)
        else:
            if isinstance(field, ThresholdOptimization):
                optimization = field
            else:
                try:
                    optimization = ThresholdOptimization.parse(field)
                except ValueError:
                    raise KeyError(field)

            return optimization.optimize_from(self)

    def format_str(self, path_tree, ndigits=3, threshold_ndigits=5, **kwargs):
        table_data = []
        if len(path_tree) == 0:
            def key_func(t_pstats):
                return util.round(t_pstats[0], threshold_ndigits)
            for threshold, t_pstats in groupby(self, key=key_func):
                _, pstats = next(t_pstats)  # Get the first item in the group
                table_data.append(
                    [util.round(threshold, threshold_ndigits)] +
                    [util.round(pstats[field], ndigits)
                     for field in ScaledPredictionStatistics.FIELDS])
                sum(1 for _ in t_pstats)  # Clear the group
            return tabulate(
                table_data,
                headers=['threshold'] + ScaledPredictionStatistics.FIELDS)
        else:
            formatted = ""
            for key in path_tree:
                opt = ThresholdOptimization.parse(key)
                threshold_tstats = opt.get_optimal(self)
                if threshold_tstats is None:
                    formatted += "{0} @ n/a\n".format(opt)
                else:
                    threshold, tstats = threshold_tstats
                    formatted += "{0} @ {1}\n".format(
                        opt, util.round(threshold,
                                        threshold_ndigits))
                    formatted += util.tab_it_in(
                        tstats.format_str({}, ndigits=3, **kwargs))
            return formatted

    def format_json(self, path_tree, ndigits=3, threshold_ndigits=5, **kwargs):

        doc = []
        if len(path_tree) == 0:
            def key_func(t_pstats):
                return util.round(t_pstats[0], threshold_ndigits)
            for rounded_threshold, t_pstats in groupby(self, key=key_func):
                _, pstats = next(t_pstats)  # Get the first item in the group
                pstats_doc = pstats.format_json({}, ndigits=3, **kwargs)
                pstats_doc['threshold'] = rounded_threshold
                pstats_doc.move_to_end('threshold', last=False)
                doc.append(pstats_doc)
                sum(1 for _ in t_pstats)  # Clear the group
        else:
            for key in path_tree:
                opt = ThresholdOptimization.parse(key)
                threshold_tstats = opt.get_optimal(self)
                if threshold_tstats is None:
                    doc.append(None)
                else:
                    threshold, tstats = threshold_tstats
                    tstats_doc = tstats.format_json(
                        path_tree[key], ndigits=3, **kwargs)
                    tstats_doc['threshold'] = threshold
                    tstats_doc.move_to_end('threshold', last=False)
                    doc.append(tstats_doc)

        return doc


def zero_to_one_auc(x_vals, y_vals):
    x_space = linspace(0, 1, 50)
    if all(diff(x_vals) > 0):
        y_interp = interp(x_space, x_vals, y_vals)
    else:
        y_interp = interp(
            x_space, list(reversed(x_vals)), list(reversed(y_vals)))
    val = auc(x_space, y_interp)
    if isnan(val):
        return None
    else:
        return val
