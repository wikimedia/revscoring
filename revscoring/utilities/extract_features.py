"""
Adds features to a set of labeled revisions.

Reads a TSV file of <rev_id>\t<label> pairs and replaces the
<rev_id> field the extracted feature values.

Input: <rev_id>[TAB]<label>


Output: <feature_1>[TAB]<feature_2>[TAB]...[TAB]<label>

Usage:
    add_features -h | --help
    add_features <features> --api=<url> [--language=<classpath>]
                                        [--rev-labels=<path>]
                                        [--verbose]

Options:
    -h --help               Print this documentation
    <features>              Classpath to a list/tuple of features
    --api=<url>             The url pointing to a MediaWiki API to use
                            for extracting features
    --language=<classpath>  Classpath to a language
    --rev-labels=<path>     Path to a file containing rev_id-label pairs
                            [default: <stdin>]
    --verbose               Print logging information
"""
import logging
import sys
import traceback

import docopt
from mw import api

from ..extractors import APIExtractor
from .util import import_from_path


def main():
    args = docopt.docopt(__doc__)

    if args['--rev-labels'] == "<stdin>":
        rev_labels = read_rev_labels(sys.stdin)
    else:
        rev_labels = read_rev_lavels(open(args['--rev-labels']))

    features = import_from_path(args['<features>'])

    if args['--language'] is None:
        language = None
    else:
        language = import_from_path(args['--language'])

    extractor = APIExtractor(api.Session(args['--api']), language=language)

    if args['--verbose']: logging.basicConfig(level=logging.DEBUG)

    run(rev_labels, features, extractor)

def read_rev_labels(f):
    for line in f:
        rev_id, label = line.strip().split('\t')
        yield int(rev_id), label

def run(rev_labels, features, extractor):

    for rev_id, label in rev_labels:

        try:
            feature_values = extractor.extract(rev_id, features)

            print("\t".join(encode(v) for v in list(feature_values) + [label]))
        except KeyboardInterrupt as e:
            sys.stderr.write("^C detected.  Shutting down.\n")
            break
        except Exception as e:
            sys.stderr.write(traceback.format_exc() + "\n")


def encode(val, none_val="NULL"):
    if val == None:
        return none_val
    elif isinstance(val, bytes):
        val = str(val, 'utf-8', "replace")
    else:
        val = str(val)

    return val.replace("\t", "\\t").replace("\n", "\\n")
