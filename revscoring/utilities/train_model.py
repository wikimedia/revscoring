"""
``revscoring train_model -h``
::

    Trains a scorer model.  This utility expects to get a file of
    tab-separated feature values and labels from which to construct a model.

    Usage:
        train_model -h | --help
        train_model <scorer_model> <features> [-p=<kv>]...
                   [--version=<vers>]
                   [--values-labels=<path>]
                   [--model-file=<path>]
                   [--label-type=<type>]
                   [--balance-sample]
                   [--balance-sample-weight]
                   [--center]
                   [--scale]
                   [--debug]

    Options:
        -h --help               Prints this documentation
        <scorer_model>          Classpath to the MLScorerModel to construct
                                and train
        <features>              Classpath to an list of features to use when
                                constructing the model
        <label>                 The name of the field to be predicted
        -p --parameter=<kv>     A key-value argument pair to use when
                                constructing the scorer_model.
        --version=<vers>        A version to associate with the model
        --observations=<path>   Path to a file containing observations
                                containing a 'cache' with <features> and a
                                <label> field [default: <stdin>]
        --model-file=<math>     Path to write a model file to
                                [default: <stdout>]
        --balance-sample         Balance the samples by sampling with
                                 replacement until all classes are equally
                                 represented
        --balance-sample-weight  Balance the weight of samples (increase
                                 importance of under-represented classes)
        --center                 Features should be centered on a common axis
        --scale                  Features should be scaled to a common range
        --debug                 Print debug logging.
"""
import json
import logging
import sys

import docopt
import yamlconf

from ..dependencies import solve
from .util import read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    sys.path.insert(0, ".")  # Search local directory first
    ScorerModel = yamlconf.import_module(args['<scorer_model>'])
    features = yamlconf.import_module(args['<features>'])

    version = args['--version']

    model_kwargs = {}
    for parameter in args['--parameter']:
        key, value = parameter.split("=")
        model_kwargs[key] = json.loads(value)

    scorer_model = ScorerModel(
        features, version=version,
        balanced_sample=args['--balance-sample'],
        balanced_sample_weight=args['--balance-sample-weight'],
        center=args['--center'],
        scale=args['--scale'],
        **model_kwargs)

    if args['--observations'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--observations']))

    label_name = args['<label>']
    value_labels = \
        [(solve(features, cache=ob['cache']), ob[label_name])
         for ob in observations]

    if args['--model-file'] == "<stdout>":
        model_file = sys.stdout.buffer
    else:
        model_file = open(args['--model-file'], 'wb')

    run(value_labels, model_file, scorer_model)


def run(value_labels, model_file, scorer_model):

    scorer_model = train_model(scorer_model, value_labels)

    sys.stderr.write(scorer_model.format_info())

    sys.stderr.write("\n\n")

    scorer_model.dump(model_file)


def train_model(scorer_model, value_labels):

    logger.debug("Train set: {0}".format(len(value_labels)))

    logger.info("Training model...")
    scorer_model.train(value_labels)

    return scorer_model
