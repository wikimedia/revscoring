"""
``revscoring score -h``
::

    Scores a set of revisions.

    Usage:
        score (-h | --help)
        score <model-file> --host=<uri> <rev_id>...
              [--caches=<json>] [--debug] [--verbose]

    Options:
        -h --help        Print this documentation
        <model-file>     Path to a model file
        --host=<url>     The url pointing to a MediaWiki API to use for
                         extracting features
        <rev_id>         A revision identifier
        --caches=<json>  A JSON blob of cache values to use during extraction
        --debug          Print debug logging
        --verbose        Print feature extraction debug logging
"""
import json
import logging

import docopt
import mwapi

from ..extractors import api
from ..scorer_models import MLScorerModel


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    model = MLScorerModel.load(open(args['<model-file>'], 'rb'))

    extractor = api.Extractor(mwapi.Session(args['--host']))

    rev_ids = [int(rev_id) for rev_id in args['<rev_id>']]

    if args['--caches'] is not None:
        caches = {int(rid): c for rid, c in
                  json.loads(args['--caches']).items()}
    else:
        caches = None

    verbose = args['--verbose']

    debug = args['--debug']

    run(model, extractor, rev_ids, caches, debug, verbose)


def run(model, extractor, rev_ids, caches, debug, verbose):

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger('requests').setLevel(logging.INFO)
    if verbose:
        logging.getLogger('revscoring.dependencies.dependent') \
               .setLevel(logging.DEBUG)
    else:
        logging.getLogger('revscoring.dependencies.dependent') \
               .setLevel(logging.INFO)

    error_features = extractor.extract(rev_ids, model.features, caches=caches)
    for rev_id, (error, values) in zip(rev_ids, error_features):
        if error is not None:
            print("\t".join([str(rev_id), str(error)]))
        else:
            score = model.score(values)
            print("\t".join([str(rev_id), json.dumps(score)]))
