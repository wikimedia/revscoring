"""
``revscoring score -h``
::

    Scores a set of revisions.

    Usage:
        score (-h | --help)
        score <model-file> <rev_id>... --host=<uri> [--verbose]

    Options:
        -h --help      Print this documentation
        <model-file>   Path to a model file
        --host=<url>   The url pointing to a MediaWiki API to use for
                       extracting features
        --verbose      Print debugging info
        <rev_id>       A revision identifier
"""
import json
import logging

import docopt

import mwapi

from ..extractors import APIExtractor
from ..scorer_models import MLScorerModel


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    model = MLScorerModel.load(open(args['<model-file>'], 'rb'))

    extractor = APIExtractor(mwapi.Session(args['--host']))

    rev_ids = [int(rev_id) for rev_id in args['<rev_id>']]

    verbose = args['--verbose']

    run(model, extractor, rev_ids, verbose)


def run(model, extractor, rev_ids, verbose):

    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
        )

    error_features = extractor.extract(rev_ids, model.features)
    for rev_id, (error, values) in zip(rev_ids, error_features):
        if error is not None:
            print("\t".join([str(rev_id), str(error)]))
        else:
            score = model.score(values)
            print("\t".join([str(rev_id), json.dumps(score)]))
