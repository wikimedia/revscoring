"""
Trains and tests a scorer model.  This utility expects to get a file of
tab-separated feature values and labels from which to construct a model.

Usage:
    train_test -h | --help
    train_test <model> <features> [--language=<module>]
                                  [--values-labels=<path>]
                                  [--boolean-labels]
                                  [--numeric-labels]

Options:
    -h --help                Prints this documentation
    <model>                  Classpath to a instance of MLScorerModel to train
    <features>               Classpath to a set of features to expect as input.
    --language=<module>      Classpath to an instance of Language
    --values-labels=<path>   Path to a file containing feature values and labels
                             [default: <stdin>]
    --boolean-labels         Interprets the labels as boolean values.
    --numeric-labels         Interprets the labels as numeric (float) values.
"""
import pprint
import random
import sys

import docopt

from .util import import_from_path


def main():
    args = docopt.docopt(__doc__)

    Model = import_from_path(args['<model>'])
    features = import_from_path(args['<features>'])

    if args['--language'] is not None:
        language = import_from_path(args['--language'])
    else:
        language = None

    model = Model(features, language=language)

    if args['--values-labels'] == "<stdin>":
        values_labels_file = sys.stdin
    else:
        values_labels_file = open(args['--values-labels'], 'r')

    boolean_labels = args['--boolean-labels']

    feature_labels = read_value_labels(values_labels_file, features,
                                       boolean_labels, numeric_labels)

    run(feature_labels, model)

def read_value_labels(f, features, boolean_labels):
    for line in f:
        parts = line.strip().split("\t")
        values = parts[:-1]
        label = parts[-1]

        if boolean_labels:
            label = label == "True"
        elif numeric_labels:
            label = float(label)

        feature_values = []
        for feature, value in zip(features, values):

            if feature.returns == bool:
                feature_values.append(value == "True")
            else:
                feature_values.append(feature.returns(value))

        yield feature_values, label

def run(feature_labels, model):

    feature_labels = list(feature_labels)
    random.shuffle(feature_labels)

    test_set_size = int(0.6*len(feature_labels))
    test_set = feature_labels[:test_set_size]
    train_set = feature_labels[test_set_size:]

    model.train(train_set)

    stats = model.test(test_set)
    del stats['roc']
    sys.stderr.write(pprint.pformat(stats) + "\n")

    model.dump(sys.stdout.buffer)

"""
./train_test \
    revscoring.scorers.LinearSVCModel \
    ores.features.enwiki.damaging \
    --language=revscoring.languages.english \
    --feature-scores=datasets/enwiki.features_reverted.20k.tsv > \
models/enwiki.reverted.linear_svc.model
"""
