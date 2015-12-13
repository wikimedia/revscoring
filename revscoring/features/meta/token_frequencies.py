from ...feature import Feature


class TokenFrequencyAggregation(Feature):
    def __init__(self, name, tf_diff_datasource, aggregate):
        self.aggregate = aggregate
        super().__init__(name, self.process, returns=float
                         depends_on=[tf_diff_datasource])

    def process(self, tf_diff_datasource):
        prop_diff = {}
        for token, delta in tf_diff.items():
            prop_diff[token] = delta / old_tf.get(token, 1)

        return prop_diff

class TokenFrequencySum(Feature):
    def __init__(self, name, tf_diff_datasource):
        super().__init__(name, self.process,
                         depends_on=[old_tf_datasource, tf_diff_datasource])

    def process(self, old_tf, tf_diff):
        prop_diff = {}
        for token, delta in tf_diff.items():
            prop_diff[token] = delta / old_tf.get(token, 1)

        return prop_diff
