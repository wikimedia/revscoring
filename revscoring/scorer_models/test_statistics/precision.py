from sklearn.metrics import precision_score
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic


class precision(ClassifierStatistic):
    """
    Constructs an accuracy generator.

    When applied to a test set, the `score()` method will return a `float`
    representing the proportion of correct predicitions.
    """
    @classmethod
    def _single_class_stat(cls, scores, labels, comparison_label):
        y_pred = [s['prediction'] == comparison_label for s in scores]
        y_true = [label == comparison_label for label in labels]

        return precision_score(y_true, y_pred)

    @classmethod
    def format(cls, precision_doc, format="str"):
        if format == "str":
            return cls.format_str(precision_doc)
        elif format == "json":
            return {label: round(precision, 3)
                    for label, precision in precision_doc.items()}
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

    @classmethod
    def format_str(cls, precision_doc):
        table_str = tabulate([[repr(label), round(p, 3)] for label, p in
                              precision_doc.items()])
        return "Precision:\n" + \
               "".join("\t" + line + "\n" for line in
                       table_str.split("\n"))

TestStatistic.register("precision", precision)
