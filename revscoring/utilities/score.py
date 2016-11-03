"""
``revscoring score -h``
::

    Scores a set of revisions.

    Usage:
        score (-h | --help)
        score <model-file> --host=<uri> [<rev_id>...]
              [--rev-ids=<path>] [--cache=<json>] [--caches=<json>]
              [--batch-size=<num>] [--io-workers=<num>] [--cpu-workers=<num>]
              [--debug] [--verbose]

    Options:
        -h --help           Print this documentation
        <model-file>        Path to a model file
        --host=<url>        The url pointing to a MediaWiki API to use for
                            extracting features
        <rev_id>            A revision identifier to score.
        --rev-ids=<path>    The path to a file containing revision identifiers
                            to score (expects a column called 'rev_id').  If
                            any <rev_id> are provided, this argument is
                            ignored. [default: <stdin>]
        --cache=<json>      A JSON blob of cache values to use during
                            extraction for every call.
        --caches=<json>     A JSON blob of rev_id-->cache value pairs to use
                            during extraction
        --batch-size=<num>  The size of the revisions to batch when requesting
                            data from the API [default: 50]
        --io-workers=<num>  The number of worker processes to use for
                            requesting data from the API [default: <auto>]
        --cpu-workers=<num>  The number of worker processes to use for
                             extraction and scoring [default: <cpu-count>]
        --debug             Print debug logging
        --verbose           Print feature extraction debug logging
"""
import json
import logging
import sys
from multiprocessing import cpu_count

import docopt
import mwapi
import mysqltsv

from ..extractors import api
from ..score_processor import ScoreProcessor
from ..scorer_models import MLScorerModel


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(
        level=logging.DEBUG if args['--debug'] else logging.WARNING,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('revscoring.dependencies.dependent') \
           .setLevel(logging.WARNING)

    model = MLScorerModel.load(open(args['<model-file>'], 'rb'))

    session = mwapi.Session(
        args['--host'],
        user_agent="Revscoring score utility <ahalfaker@wikimedia.org>")
    extractor = api.Extractor(session)

    if len(args['<rev_id>']) > 0:
        rev_ids = (int(rev_id) for rev_id in args['<rev_id>'])
    else:
        if args['--rev-ids'] == "<stdin>":
            rev_ids_f = sys.stdin
        else:
            rev_ids_f = open(args['--rev-ids'])

        rev_ids = (int(row.rev_id) for row in mysqltsv.read(rev_ids_f))

    if args['--caches'] is not None:
        caches = json.loads(args['--caches'])
    else:
        caches = None

    if args['--cache'] is not None:
        cache = json.loads(args['--cache'])
    else:
        cache = None

    batch_size = int(args['--batch-size'])

    if args['--cpu-workers'] == "<cpu-count>":
        cpu_workers = cpu_count()
    else:
        cpu_workers = int(args['--cpu-workers'])

    if args['--io-workers'] == "<auto>":
        io_workers = None
    else:
        io_workers = int(args['--io-workers'])

    verbose = args['--verbose']

    debug = args['--debug']

    score_processor = ScoreProcessor(model, extractor, batch_size=batch_size,
                                     cpu_workers=cpu_workers,
                                     io_workers=io_workers)

    run(score_processor, rev_ids, caches, cache, debug, verbose)


def run(score_processor, rev_ids, caches, cache, debug, verbose):

    rev_scores = score_processor.score(rev_ids, caches, cache)

    for rev_id, score in rev_scores:
        print("\t".join([str(rev_id), json.dumps(score)]))
        if verbose:
            if 'error' in score:
                if "NotFound" in score['error']['type']:
                    sys.stderr.write("?")
                elif "Deleted" in score['error']['type']:
                    sys.stderr.write("d")
                else:
                    sys.stderr.write("e")
            else:
                sys.stderr.write(".")
            sys.stderr.flush()
