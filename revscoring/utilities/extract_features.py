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
        extract_features <features> --api=<url> [--language=<classpath>]
                                                [--rev-labels=<path>]
                                                [--value-labels=<path>]
                                                [--verbose]

    Options:
        -h --help                Print this documentation
        <features>               Classpath to a list/tuple of features
        --api=<url>              The url pointing to a MediaWiki API to use
                                 for extracting features
        --language=<classpath>   Classpath to a Language
        --rev-labels=<path>      Path to a file containing rev_id-label pairs
                                 [default: <stdin>]
        --value-labels=<path>    Path to a file to write feature-labels to
                                 [default: <stdout>]
        --verbose                Print logging information
"""
import logging
import sys
import traceback

import docopt
from mw import api

from ..extractors import APIExtractor
from .util import encode, import_from_path


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    features = import_from_path(args['<features>'])

    if args['--language'] is None:
        language = None
    else:
        language = import_from_path(args['--language'])

    session = api.Session(args['--api'],
                          user_agent="Revscoring feature extractor utility")
    extractor = APIExtractor(session, language=language)

    if args['--rev-labels'] == "<stdin>":
        rev_labels = read_rev_labels(sys.stdin)
    else:
        rev_labels = read_rev_labels(open(args['--rev-labels']))

    if args['--value-labels'] == "<stdout>":
        value_labels = sys.stdout
    else:
        value_labels = open(args['--value-labels'], 'w')

    verbose = args['--verbose']

    run(rev_labels, value_labels, features, extractor, verbose)

def read_rev_labels(f):
    # Check if first line is a header
    rev_id, label = f.readline().strip().split("\t")
    if rev_id != "rev_id":
        yield int(rev_id), label

    for line in f:
        rev_id, label = line.strip().split('\t')
        yield int(rev_id), label

def run(rev_labels, value_labels, features, extractor, verbose=False):
    #if verbose: logging.basicConfig(level=logging.DEBUG)
    # This is far too verbose.

    for rev_id, label in rev_labels:

        try:
            values = extractor.extract(rev_id, features)
            sys.stderr.write(".");sys.stderr.flush()

            value_labels.write("\t".join(encode(v)
                                         for v in list(values) + [label]))
            value_labels.write("\n")
        except KeyboardInterrupt as e:
            sys.stderr.write("^C detected.  Shutting down.\n")
            break
        except Exception as e:
            sys.stderr.write(traceback.format_exc() + "\n")

    sys.stderr.write("\n")
