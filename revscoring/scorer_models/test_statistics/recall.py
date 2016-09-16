from sklearn.metrics import recall_score
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic


class recall(ClassifierStatistic):
    """
    Constructs an accuracy generator.

    When applied to a test set, the `score()` method will return a `float`
    representing the proportion of correct predicitions.
    """
    @classmethod
    def _single_class_stat(cls, scores, labels, comparison_label):
        y_pred = [s['prediction'] == comparison_label for s in scores]
        y_true = [label == comparison_label for label in labels]

        return recall_score(y_true, y_pred)

    @classmethod
    def format(cls, recall_doc, format="str"):
        if format == "str":
            return cls.format_str(recall_doc)
        elif format == "json":
            return {label: round(recall, 3)
                    for label, recall in recall_doc.items()}
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

    @classmethod
    def format_str(cls, recall_doc):
        table_str = tabulate([[repr(label), round(r, 3)]
                              for label, r in recall_doc.items()])
        return "Recall:\n" + \
               "".join("\t" + line + "\n" for line in
                       table_str.split("\n"))

TestStatistic.register("recall", recall)
