"""
.. autoclass:: revscoring.scoring.Statistics
    :members:
    :member-order:

.. autofunc:: revscoring.scoring.statistics.parse_pattern
"""

import logging

logger = logging.getLogger(__name__)


class Statistics(dict):

    def __init__(self):
        """
        Construct a set of Statistics.  Instances of this class work like a
        `dict` of statistical values once
        :func:`revscoring.scoring.Statistics.fit` is called.
        """
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

    def lookup(self, pattern_or_path):
        """
        Looks up a specific statistical value based on either a string pattern
        or a path.

        For example, the pattern "roc_auc.labels.true" is the same as the path
        `['roc_auc', 'labels', True]`.

        :Parameters:
            pattern_or_path : `str` | `list`
                The location of the statistic to lookup.
        """
        if isinstance(pattern_or_path, str):
            path = parse_pattern(pattern_or_path)
        else:
            path = pattern_or_path

        d = self
        for key in path:
            try:
                d = d[key]
            except KeyError as e:
                if key in ("true", "false"):
                    d = d[key == 'true']
                else:
                    try:
                        d = d[int(key)]
                    except ValueError:
                        raise e
        return d

    def format_str(self, *args, **kwargs):
        raise NotImplementedError()

    def format_json(self, *args, **kwargs):
        raise NotImplementedError()

    def format(self, *args, formatting="str", **kwargs):
        """
        Format a representation of the statistics information in a useful way.

        :Parameters:
            formatting : "json" or "str"
                Which output formatting do you want?  "str" returns something
                nice to show on the command-line.  "json" returns something
                that will pass through :func:`json.dump` without error.
            fields : [ `str` ]
                A list of keys for statistics that should be included in the
                output.
            ndigits : int
                How many digits should statistics and other information be
                rounded to.
        """
        if formatting == "str":
            return self.format_str(*args, **kwargs)
        elif formatting == "json":
            return self.format_json(*args, **kwargs)
        else:
            raise ValueError("Unknown formatting {0!r}".format(formatting))


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
