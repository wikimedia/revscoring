from sklearn.metrics import f1_score
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic


class f1(ClassifierStatistic):
    """
    Constructs an F1 score generator.

    When applied to a test set, the `score()` method will return a `float`
    representing the balanced F-score or F-measure.
    """
    @classmethod
    def _single_class_stat(cls, scores, labels, comparison_label):
        y_pred = [s['prediction'] == comparison_label for s in scores]
        y_true = [label == comparison_label for label in labels]

        return f1_score(y_true, y_pred)

    @classmethod
    def format(cls, f1_doc, format="str"):
        if format == "str":
            return cls.format_str(f1_doc)
        elif format == "json":
            if isinstance(f1_doc, float):
                return round(f1_doc, 3)
            else:
                return {label: round(f1_score, 3)
                        for label, f1_score in f1_doc.items()}
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

    @classmethod
    def format_str(cls, recall_doc):
        if isinstance(recall_doc, float):
            return "F1: {0}".format(round(recall_doc, 3))
        else:
            table_str = tabulate([[l, round(r, 3)] for l, r in
                                  recall_doc.items()])
            return "F1:\n" + \
                   "".join("\t" + line + "\n" for line in
                           table_str.split("\n"))

TestStatistic.register("f1", f1)
