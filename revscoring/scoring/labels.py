from itertools import chain

from .. import errors


class Normalizer:

    def check_consistency_and_normalize(self, labels):
        self.check_label_consistency(labels)
        return [self.normalize(l) for l in labels]

    def normalize(self, label):
        raise NotImplementedError()

    def denormalize(self, normalized_label):
        raise NotImplementedError()


class ClassVerifier(Normalizer):

    def __init__(self, possible_labels):
        self.label_set = set(possible_labels)

    def check_label_consistency(self, labels):
        unique_labels = set(labels)
        if unique_labels - self.label_set:
            raise errors.ModelConsistencyError(
                "Labels {0} not in expected labels {1}"
                .format(unique_labels - self.label_set, self.label_set))
        elif self.label_set - unique_labels:
            raise errors.ModelConsistencyError(
                "Expected labels {0} represented"
                .format(self.label_set - unique_labels))

    def normalize(self, label):
        if label not in self.label_set:
            raise errors.ModelConsistencyError(
                "Label {0} not in list of expected labels {1}"
                .format(label, self.label_set))
        else:
            return label

    def denormalize(self, label):
        return label


class Binarizer(ClassVerifier):

    def __init__(self, possible_labels):
        super().__init__(possible_labels)
        self.label_index_map = {l: i for i, l in enumerate(possible_labels)}
        self.possible_labels = possible_labels

    def check_label_consistency(self, labels):
        unique_labels = set(chain(*(l for l in labels)))
        super().check_label_consistency(unique_labels)

    def normalize(self, label_set):
        binary_map = [0 for i in range(len(self.possible_labels))]
        for l in label_set:
            try:
                index = self.label_index_map[l]
            except KeyError:
                raise errors.ModelConsistencyError(
                    "Label {0} not in list of expected labels {1}"
                    .format(l, self.possible_labels))
            binary_map[index] = 1
        return binary_map

    def denormalize(self, binary_map):
        label_set = []
        for index, val in enumerate(binary_map):
            if val:
                label_set.append(self.possible_labels[index])

        return label_set
