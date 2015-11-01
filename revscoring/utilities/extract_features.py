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
                                                 [--include-revid]
                                                 [--extractors=<num>]
                                                 [--verbose] [--debug]

    Options:
        -h --help               Print this documentation
        <features>              Classpath to a list/tuple of features
        --host=<url>            The url pointing to a MediaWiki API to use
                                for extracting features
        --rev-labels=<path>     Path to a file containing rev_id-label pairs
                                [default: <stdin>]
        --value-labels=<path>   Path to a file to write feature-labels to
                                [default: <stdout>]
        --include-revid         If set, include the revision ID as the first
                                column in the output TSV
        --extractors=<num>      The number of extractors to run in parallel
                                [default: <cpu count>]
        --verbose               Print dots and stuff
        --debug                 Print debug logging
"""
import logging
import sys
from itertools import islice
from multiprocessing import Pool, cpu_count

import docopt
import mwapi

from ..errors import RevisionNotFound
from ..extractors import APIExtractor
from .util import encode, import_from_path

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

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

    include_revid = bool(args['--include-revid'])

    if args['--extractors'] == "<cpu count>":
        extractors = cpu_count()
    else:
        extractors = int(extractors)

    verbose = args['--verbose']
    debug = args['--debug']

    run(rev_labels, value_labels, features, extractor, include_revid,
        extractors, verbose, debug)


def read_rev_labels(f):
    # Check if first line is a header
    rev_id, label = f.readline().strip().split("\t")
    if rev_id != "rev_id":
        yield int(rev_id), label

    for line in f:
        rev_id, label = line.strip().split('\t')
        yield int(rev_id), label


def run(rev_labels, value_labels, features, extractor, include_revid,
        extractors, verbose, debug):
    logging.basicConfig(
        level=logging.WARNING if not debug else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    extractor_context = ConfiguredExtractor(extractor, features)
    extractor_pool = Pool(processes=extractors)

    error_rev_label_features = extractor_pool.imap(extractor_context.extract,
                                                   rev_labels)

    for error, rev_id, label, feature_values in error_rev_label_features:
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
            fields = list(feature_values) + [label]

            if include_revid:
                fields = [rev_id] + fields

            value_labels.write("\t".join(encode(v)
                                         for v in fields))
            value_labels.write("\n")

            if verbose:
                sys.stderr.write(".")
                sys.stderr.flush()

    if verbose:
        sys.stderr.write("\n")


class ConfiguredExtractor:

    def __init__(self, extractor, features):
        self.extractor = extractor
        self.features = features

    def extract(self, rev_label):
        rev_id, label = rev_label
        try:
            feature_values = list(self.extractor.extract(rev_id, self.features))
            error = None
        except Exception as e:
            feature_values = None
            error = e

        return error, rev_id, label, feature_values
