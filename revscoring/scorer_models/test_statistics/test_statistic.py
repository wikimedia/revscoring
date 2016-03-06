import json
import re

# TODO: This regex fails when commas are used for anything but delimiting
KWARG_STR_RE = re.compile(r"\s*([a-z_][a-z_0-9]*)" +  # 1/1 keyword
                          r"\s*=\s*" +
                          r"([^,\)]+)\s*" +  # 2/2 value
                          r"(,\s*)?")  # 3/3 comma separated

STAT_STR_RE = re.compile(r"\s*([a-z_][a-z_0-9]*)" +  # 1/1 statistic
                         r"(\s*\(" +  # 2 parameters
                            "(" + KWARG_STR_RE.pattern + r")+" +  # 3
                         r"\))?\s*")  # 2 parameters


class TestStatistic:
    """
    Represents a test statistic.
    """
    STATISTICS = {}

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def score(self, scores, labels):
        raise NotImplementedError()

    def format(self, stats):
        raise NotImplementedError()

    def __repr__(self):
        if len(self.kwargs) > 0:
            args = "({0})".format(", ".join(k + "=" + repr(v) for k, v in
                                  self.kwargs.items()))
        else:
            args = ""

        return "{0}{1}".format(self.__class__.__name__, args)

    def __str__(self):
        return self.__repr__()

    def hash(self):
        return hash(self.__str__())

    @classmethod
    def from_stat_str(cls, param_str):
        stat_match = STAT_STR_RE.match(param_str)
        if not stat_match:
            raise ValueError("Malformated statistic string ")
        else:

            kwarg_str = stat_match.group(2) or ""
            class_name = stat_match.group(1)

            if class_name not in cls.STATISTICS:
                raise ValueError("Statistic '{0}' not available"
                                 .format(class_name))
            kwargs = {}
            for kwarg_match in KWARG_STR_RE.finditer(kwarg_str):
                name = kwarg_match.group(1)
                value = json.loads(kwarg_match.group(2))
                kwargs[name] = value

            return cls.STATISTICS[class_name](**kwargs)

    @classmethod
    def register(cls, name, Statistic):
        cls.STATISTICS[name] = Statistic


class ClassifierStatistic(TestStatistic):
    """
    Represents a test statistic for classifier models.
    """
    def score(self, scores, labels):
        if set(labels) == {True, False}:
            return self._single_class_stat(scores, labels, True)
        else:
            score = {}
            for comparison_label in set(labels):
                score[comparison_label] = \
                    self._single_class_stat(scores, labels, comparison_label)

            return score
