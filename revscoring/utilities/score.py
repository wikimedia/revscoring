"""
Scores a set of revisions.

Usage:
    score (-h | --help)
    score <model-file> <rev_id>... --api=<uri> [--verbose]

Options:
    -h --help      Print this documentation
    <model-file>   Path to a model file
    --api=<url>    The url pointing to a MediaWiki API to use for extracting
                   features
    --verbose      Print debugging info
    <rev_id>       A revision identifier
"""
import json
import logging
import sys
import traceback

import docopt
from mw import api

from ..extractors import APIExtractor
from ..scorers import MLScorerModel, Scorer


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    model = MLScorerModel.load(open(args['<model-file>'], 'rb'))

    extractor = APIExtractor(api.Session(args['--api']),
                             language=model.language)

    scorer = Scorer({'model': model}, extractor)

    rev_ids = [int(rev_id) for rev_id in args['<rev_id>']]

    verbose = args['--verbose']

    run(scorer, rev_ids, verbose)

def run(scorer, rev_ids, verbose):

    if verbose: logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    for rev_id, score in zip(rev_ids, scorer.score_many(rev_ids)):
        print("\t".join([str(rev_id), json.dumps(score)]))
