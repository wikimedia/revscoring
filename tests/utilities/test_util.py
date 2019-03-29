from revscoring.utilities.util import (read_labels_and_population_rates,
                                       read_labels_config)


def test_plain_labels():
    labels, label_weights, population_rates = read_labels_and_population_rates(
        "true,false", ["true=5"], ["true=0.1", "false=0.9"], None)

    assert labels == [True, False]
    assert label_weights == {True: 5}
    assert population_rates == {True: 0.1, False: 0.9}


def test_pop_rates_labels():
    labels, label_weights, population_rates = read_labels_and_population_rates(
         None, ["true=5"], ["true=0.1", "false=0.9"], None)

    assert labels == [True, False]
    assert label_weights == {True: 5}
    assert population_rates == {True: 0.1, False: 0.9}


def test_labels_config():
    labels_config = {
        'name': "enwiki damaging",
        'labels': [
            {'value': True, 'weight': 5, 'population_rate': 0.1},
            {'value': False, 'population_rate': 0.9}
        ]}
    labels, label_weights, population_rates = read_labels_config(labels_config)

    assert labels == [True, False]
    assert label_weights == {True: 5}
    assert population_rates == {True: 0.1, False: 0.9}
