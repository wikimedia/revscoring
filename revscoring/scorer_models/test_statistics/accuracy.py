from sklearn.metrics import accuracy_score

from .test_statistic import ClassifierStatistic, TestStatistic


class accuracy(ClassifierStatistic):
    """
    Constructs an accuracy generator.

    When applied to a test set, the `score()` method will return a `float`
    representing the proportion of correct predicitions.
    """

    def score(self, scores, labels):
        y_pred = [s['prediction'] for s, l in zip(scores, labels)]

        return accuracy_score(labels, y_pred)

    def format(cls, accuracy_doc, format="str"):

        rounded_accuracy = round(accuracy_doc, 3)

        if format == "str":
            return "Accuracy: {0}".format(rounded_accuracy)
        elif format == "json":
            return rounded_accuracy
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

TestStatistic.register("accuracy", accuracy)
