"""
.. autoclass:: revscoring.scoring.Statistics
    :members:
    :member-order:

.. autofunc:: revscoring.scoring.statistics.parse_pattern
"""
import logging

from ..model_info import ModelInfo

logger = logging.getLogger(__name__)


class Statistics(ModelInfo):

    def __init__(self):
        """
        Construct a set of Statistics.  Instances of this class work like a
        `dict` of statistical values once
        :func:`revscoring.scoring.Statistics.fit` is called.
        """
        super().__init__()
        self.fitted = False

    def fit(self, score_labels):
        """
        Fit to scores and labels.

        :Parameters:
            score_labels : [( `dict`, `mixed` )]
                A collection of scores-label pairs generated using
                :class:`revscoring.Model.score`.  Note that fitting is usually
                done using data withheld during model training
        """
        self.fitted = True

    def format_str(self, path_tree, **kwargs):
        raise NotImplementedError()

    def format_json(self, path_tree, **kwargs):
        raise NotImplementedError()


def parse_pattern(string):
    """
    Parse a statistic lookup pattern
    """
    return list(_parse_pattern(string))


def _parse_pattern(string):
    parts = string.split(".")
    buf = []
    for part in parts:
        if buf:
            if part[-1] in ('"', "'") and part[-1] == buf[0][0]:
                yield (''.join(buf + [part])).strip("'\"")
                buf = []
            else:
                buf.append(part + ".")
        elif part[0] in ('"', "'"):
            if part[-1] in ('"', "'") and part[0] == part[-1]:
                yield part.strip("'\"")
            else:
                buf.append(part + ".")
        else:
            yield part

    if buf:
        raise ValueError("Parsing error unmatching quotes {0}"
                         .format(''.join(buf)))
