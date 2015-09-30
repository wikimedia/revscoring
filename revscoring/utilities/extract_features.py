"""
``revscoring extract_features -h``
::

    Adds features to a set of labeled revisions.

    Reads a TSV file of <rev_id>\t<label> pairs and replaces the
    <rev_id> field with the extracted feature values.

    Input: <rev_id>[TAB]<label>

    Output: <feature_1>[TAB]<feature_2>[TAB]...[TAB]<label>


    Usage:
        extract_features -h | --help
        extract_features <features> --host=<url> [--rev-labels=<path>]
                                                 [--value-labels=<path>]
                                                 [--verbose] [--debug]

    Options:
        -h --help                Print this documentation
        <features>               Classpath to a list/tuple of features
        --host=<url>             The url pointing to a MediaWiki API to use
                                 for extracting features
        --rev-labels=<path>      Path to a file containing rev_id-label pairs
                                 [default: <stdin>]
        --value-labels=<path>    Path to a file to write feature-labels to
                                 [default: <stdout>]
        --verbose                Print dots and stuff
        --debug                  Print debug logging
"""
import logging
import sys
from itertools import islice

import docopt
import mwapi

from ..errors import RevisionNotFound
from ..extractors import APIExtractor
from .util import encode, import_from_path

logger = logging.getLogger(__name__)

BATCH_SIZE = 50


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    features = import_from_path(args['<features>'])

    session = mwapi.Session(args['--host'],
                            user_agent="Revscoring feature extractor utility")
    extractor = APIExtractor(session)

    if args['--rev-labels'] == "<stdin>":
        rev_labels = read_rev_labels(sys.stdin)
    else:
        rev_labels = read_rev_labels(open(args['--rev-labels']))

    if args['--value-labels'] == "<stdout>":
        value_labels = sys.stdout
    else:
        value_labels = open(args['--value-labels'], 'w')

    verbose = args['--verbose']
    debug = args['--debug']

    run(rev_labels, value_labels, features, extractor, verbose, debug)


def read_rev_labels(f):
    # Check if first line is a header
    rev_id, label = f.readline().strip().split("\t")
    if rev_id != "rev_id":
        yield int(rev_id), label

    for line in f:
        rev_id, label = line.strip().split('\t')
        yield int(rev_id), label


def run(rev_labels, value_labels, features, extractor, verbose, debug):
    logging.basicConfig(
        level=logging.WARNING if not debug else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    while True:
        batch_rev_labels = list(islice(rev_labels, BATCH_SIZE))
        if len(batch_rev_labels) == 0:
            break

        rev_ids, labels = zip(*batch_rev_labels)

        error_values_label = zip(extractor.extract(rev_ids, features),
                                 batch_rev_labels)
        for (error, values), (rev_id, label) in error_values_label:
            try:
                if isinstance(error, RevisionNotFound):
                    if verbose:
                        sys.stderr.write("?")
                        sys.stderr.flush()
                elif error is not None:
                    logger.error("An error occured while processing {0}:"
                                 .format(rev_id))
                    logger.error("\t{0}: {1}"
                                 .format(error.__class__.__name__,
                                         str(error)))
                else:
                    fields = list(values) + [label]
                    value_labels.write("\t".join(encode(v)
                                                 for v in fields))
                    value_labels.write("\n")

                    if verbose:
                        sys.stderr.write(".")
                        sys.stderr.flush()

            except KeyboardInterrupt:
                sys.stderr.write("^C detected.  Shutting down.\n")
                break

    if verbose:
        sys.stderr.write("\n")
