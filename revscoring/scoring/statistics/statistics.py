import logging

logger = logging.getLogger(__name__)


class Statistics(dict):

    def __init__(self):
        self.fitted = False

    def fit(self, score_labels):
        self.fitted = True

    def format_str(self, ndigits=3):
        raise NotImplementedError()

    def format_json(self, ndigits=3):
        raise NotImplementedError()

    def format(self, *args, formatting="str", **kwargs):
        if formatting == "str":
            return self.format_str(*args, **kwargs)
        elif formatting == "json":
            return self.format_json(*args, **kwargs)
        else:
            raise ValueError("Unknown formatting {0!r}".format(formatting))
