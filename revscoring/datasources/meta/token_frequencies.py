from ...datasources import Datasource


class TokenFrequency(Datasource):

    def __init__(self, name, tokens_datasource, if_none=None):
        self.if_none = if_none
        super().__init__(name, self.process,
                         depends_on=[tokens_datasource])

    def process(self, tokens):
        if tokens is None:
            if self.if_none is not None:
                return self.if_none()
            else:
                return {}

        freq = {}
        for token in tokens:
            if token in freq:
                freq[token] += 1
            else:
                freq[token] = 1

        return freq


class TokenFrequencyDiff(Datasource):

    def __init__(self, name, old_tf_datasource, new_tf_datasource,
                 if_none=None):
        self.if_none = if_none
        super().__init__(name, self.process,
                         depends_on=[old_tf_datasource, new_tf_datasource])

    def process(self, old_tf, new_tf):
        old_tf = old_tf or {}

        if new_tf is None:
            if self.if_none is not None:
                return self.if_none()
            else:
                return {}

        tf_diff = {}
        for token, new_count in new_tf.items():
            old_count = old_tf.get(token, 0)
            if new_count != old_count:
                tf_diff[token] = new_count - old_count

        for token in old_tf.keys() - new_tf.keys():
            tf_diff[token] = old_tf[token] * -1

        return tf_diff


class ProportionalTokenFrequencyDiff(Datasource):

    def __init__(self, name, old_tf_datasource, tf_diff_datasource):
        super().__init__(name, self.process,
                         depends_on=[old_tf_datasource, tf_diff_datasource])

    def process(self, old_tf, tf_diff):
        prop_diff = {}
        for token, delta in tf_diff.items():
            prop_diff[token] = delta / old_tf.get(token, 1)

        return prop_diff
