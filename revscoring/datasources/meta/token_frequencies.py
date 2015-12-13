from ..datasource import Datasource


class frequency(Datasource):

    def __init__(self, name, items_datasource):
        name = self.format_name(name, [items_datasource])
        super().__init__(name, self.process,
                         depends_on=[items_datasource])

    def process(self, items):

        freq = {}
        for item in items:
            if item in freq:
                freq[item] += 1
            else:
                freq[item] = 1

        return freq


class frequency_diff(Datasource):

    def __init__(self, name, old_tf_datasource, new_tf_datasource):
        name = self.format_name(name, [old_tf_datasource, new_tf_datasource])
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


class prop_frequency_diff(Datasource):

    def __init__(self, name, old_tf_datasource, tf_diff_datasource):
        name = self.format_name(name, [old_tf_datasource, tf_diff_datasource])
        super().__init__(name, self.process,
                         depends_on=[old_tf_datasource, tf_diff_datasource])

    def process(self, old_tf, tf_diff):
        prop_diff = {}
        for token, delta in tf_diff.items():
            prop_diff[token] = delta / old_tf.get(token, 1)

        return prop_diff
