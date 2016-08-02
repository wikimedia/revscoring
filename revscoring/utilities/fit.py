"""
``revscoring fit -h``
::
    Fits a dependent (an extractable value like a Datasource or Feature) to
    observed data.  These are often used along with bag-of-words
    methods to reduce the feature space prior to training and testing a model
    or to train a sub-model.

    Usage:
        fit -h | --help
        fit <dependent> <label>
            [--input=<path>]
            [--datasource-file=<path>]
            [--debug]

    Options:
        -h --help                 Prints this documentation
        <dependent>               The classpath to `Dependent`
                                  that can be fit to observations
        <label>                   The label that should be predicted
        --input=<path>            Path to a file containing observations
                                  [default: <stdin>]
        --datasource-file=<math>  Path to a file for writing out the trained
                                  datasource [default: <stdout>]
        --debug                   Print debug logging.
"""
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

    dependent = yamlconf.import_path(args['<dependent>'])

    label_name = args['<label>']

    if args['--input'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--input']))

    logger.info("Reading observations...")
    value_labels = [
        (list(solve(dependent.dependencies, cache=ob['cache'])),
         ob[label_name])
         for ob in observations]
    logger.debug(" -- {0} observations gathered".format(len(value_labels)))

    if args['--datasource-file'] == "<stdout>":
        datasource_f = sys.stdout
    else:
        datasource_f = open(args['--datasource-file'], 'w')

    debug = args['--debug']

    run(dependent, label_name, value_labels, datasource_f, debug)


def run(dependent, label_name, value_labels, datasource_f, debug):
    logger.info("Fitting {0} ({1})".format(dependent, type(dependent)))
    dependent.fit(value_labels)

    logger.info("Writing fitted selector to {0}".format(datasource_f))
    dependent.dump(datasource_f)
