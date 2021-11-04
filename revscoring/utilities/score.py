"""
``revscoring score -h``
::

    Scores a set of revisions.

    Usage:
        score (-h | --help)
        score <model-file> --host=<uri> [<rev_id>...]
              [--rev-docs=<path>] [--output=<path>]
              [--cache=<json>] [--caches=<json>]
              [--score-field=<key>]
              [--batch-size=<num>] [--io-workers=<num>] [--cpu-workers=<num>]
              [--debug] [--verbose]

    Options:
        -h --help           Print this documentation
        <model-file>        Path to a model file
        --host=<url>        The url pointing to a MediaWiki API to use for
                            extracting features
        <rev_id>            A revision identifier to score.
        --rev-docs=<path>   The path to a file containing json blobs with a
                            "rev_id" field to score.  If any <rev_id> are
                            provided, this argument is ignored.
                            [default: <stdin>]
        --output=<path>     Path to a file to write rev_docs with score data to
                            [default: <stdout>]
        --cache=<json>      A JSON blob of cache values to use during
                            extraction for every call.
        --caches=<json>     A JSON blob of rev_id-->cache value pairs to use
                            during extraction
        --score-field=<key> The field name that the score will be inserted into
                            [default: score]
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
from more_itertools import chunked

from ..extractors import api
from ..score_processor import ScoreProcessor
from ..scoring import Model, models
from .util import read_observations, dump_observation


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)
    logging.basicConfig(
        level=logging.DEBUG if args['--debug'] else logging.WARNING,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('revscoring.dependencies.dependent') \
           .setLevel(logging.WARNING)

    scoring_model = Model.load(models.open_file(args['<model-file>']))

    session = mwapi.Session(
        args['--host'],
        user_agent="Revscoring score utility <ahalfaker@wikimedia.org>")
    extractor = api.Extractor(session)

    if len(args['<rev_id>']) > 0:
        rev_docs = ({'rev_id': int(rev_id)} for rev_id in args['<rev_id>'])
    else:
        if args['--rev-docs'] == "<stdin>":
            rev_docs = read_observations(sys.stdin)
        else:
            rev_docs = read_observations(open(args['--rev-ids']))

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(args['--output'], 'w')

    if args['--caches'] is not None:
        caches = json.loads(args['--caches'])
    else:
        caches = None

    if args['--cache'] is not None:
        cache = json.loads(args['--cache'])
    else:
        cache = None

    score_field = args['--score-field']

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

    score_processor = ScoreProcessor(
        scoring_model, extractor, batch_size=batch_size,
        cpu_workers=cpu_workers, io_workers=io_workers)

    run(score_processor, rev_docs, output, caches, cache, score_field, io_workers, debug, verbose)


def run(score_processor, rev_docs, output, caches, cache, score_field, io_workers, debug, verbose):

    for rev_doc_chunk in chunked(rev_docs, 50 * score_processor.io_workers):
        rev_doc_chunk = list(rev_doc_chunk)
        rev_ids = [r['rev_id'] for r in rev_doc_chunk]
        rev_scores = score_processor.score(rev_ids, caches, cache)

        for rev_doc, (rev_id, score) in zip(rev_doc_chunk, rev_scores):
            rev_doc[score_field] = score
            dump_observation(rev_doc, output)

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
