"""
Scores a set of revisions.

Usage:
    score (-h | --help)
    score <model-file> <rev_id>... --api=<uri>

Options:
    -h --help      Print this documentation
    <model-file>   Path to a model file
    --api=<url>    The url pointing to a MediaWiki API to use for extracting
                   features
    <rev_id>       A revision identifier
"""
import json
import sys
import traceback

import docopt
from mw import api

from ..extractors import APIExtractor
from ..scorers import MLScorerModel


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    model = MLScorerModel.load(open(args['<model-file>'], 'rb'))

    extractor = APIExtractor(api.Session(args['--api']),
                             language=model.language)

    rev_ids = [int(rev_id) for rev_id in args['<rev_id>']]

    run(model, extractor, rev_ids)

def run(model, extractor, rev_ids):
    for rev_id in rev_ids:
        try:
            features = extractor.extract(rev_id, model.features)
            score_doc = model.score(features)
            print("\t".join([str(rev_id), json.dumps(score_doc)]))
        except Exception as e:
            print("\t".join([str(rev_id), json.dumps(None)]))
            sys.stderr.write(traceback.format_exc())
