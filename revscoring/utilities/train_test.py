"""
Trains and tests a scorer model.  This utility expects to get a file of
tab-separated feature values and labels from which to construct a model.

Usage:
    train_test -h | --help
    train_test <model> [--language=<module>]
                       [--values-labels=<path>]
                       [--model-file=<path>]
                       [--label-type=<type>]

Options:
    -h --help                Prints this documentation
    <model>                  Classpath to an instance of MLScorerModel to train
    --values-labels=<path>   Path to a file containing feature values and labels
                             [default: <stdin>]
    --model-file=<math>      Path to write a model file to [default: <stdout>]
    --label-type=<type>      Interprets the labels as the appropriate type
                             (int, float, str, bool) [default: str]
"""
import pprint
import random
import sys

import docopt

from .util import encode, import_from_path


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    model = import_from_path(args['<model>'])

    if args['--values-labels'] == "<stdin>":
        values_labels_file = sys.stdin
    else:
        values_labels_file = open(args['--values-labels'], 'r')

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    decode_label = DECODERS[args['--label-type']]

    feature_labels = read_value_labels(values_labels_file, model.features,
                                       decode_label)

    run(feature_labels, model_file, model)

DECODERS = {
    'int': lambda v: int(v),
    'float': lambda v: float(v),
    'str': lambda v: str(v),
    'bool': lambda v: v in ("True", "true", "1", "T", "y", "Y")
}

def read_value_labels(f, features, decode_label):
    for line in f:
        parts = line.strip().split("\t")
        values = parts[:-1]
        label = parts[-1]

        label = decode_label(label)

        feature_values = []
        for feature, value in zip(features, values):

            if feature.returns == bool:
                feature_values.append(value == "True")
            else:
                feature_values.append(feature.returns(value))

        yield feature_values, label

def run(feature_labels, model_file, model):

    feature_labels = list(feature_labels)
    random.shuffle(feature_labels)

    test_set_size = int(0.6*len(feature_labels))
    test_set = feature_labels[:test_set_size]
    train_set = feature_labels[test_set_size:]

    model.train(train_set)

    stats = model.test(test_set)
    del stats['roc']
    sys.stderr.write(pprint.pformat(stats) + "\n")

    model.dump(model_file)
