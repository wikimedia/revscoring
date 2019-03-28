from revscoring.scoring.labels import Binarizer, ClassVerifier


def test_class_verifier():
    label_set = [True, False]
    cv = ClassVerifier(label_set)
    labels = [True, True, False, True, False, False]
    cv.check_label_consistency(labels)
    normalized_labels = cv.normalize(True)
    assert normalized_labels


def test_binarizer():
    label_set = ['A', 'B', 'C', 'D']
    labels = [['A', 'B'], ['B', 'D'], ['A', 'B', 'C', 'D'], ['B', 'C']]
    binarizer = Binarizer(label_set)
    binarizer.check_label_consistency(labels)
    normalized_labels = binarizer.normalize(labels[1])
    normalized_labels_actual = [0, 1, 0, 1]
    assert normalized_labels == normalized_labels_actual

    denormalized_labels = binarizer.denormalize(normalized_labels_actual)
    assert denormalized_labels == labels[1]


def test_label_weights_normalizer():
    label_weights = {'A': 0.4, 'B': 0.6}
    label_set = ['A', 'B']
    binarizer = Binarizer(label_set)
    expected_label_weights = [{0: 1, 1: 0.4}, {0: 1, 1: 0.6}]
    assert expected_label_weights == \
        binarizer.normalize_weights(label_weights)
