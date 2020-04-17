"""
``revscoring fetch_text -h``
::

    Gets the text for a set of observations.  Will create a new field called
    "text" with the content corresponding to the "rev_id".

    Usage:
        fetch_text --host=<url>
                   [--deleted-1st]
                   [--login]
                   [--input=<path>] [--output=<path>]
                   [--threads=<num>]
                   [--verbose] [--debug]

    Options:
        -h --help        Print this documentation
        --host=<url>     The host URL of a MediaWiki installation to extract
                         text from
        --deleted-1st    Try to look up text in "deletedrevisions" first.
                         This is more performant when looking up text that
                         will be (mostly) deleted, but it will have no effect
                         on output.
        --login          If set, prompt the user to log in.
        --input=<path>   Path to a file containing observations
                         [default: <stdin>]
        --output=<path>  Path to a file to write extended observations
                         [default: <stdout>]
        --threads=<num>  The number of parallel requests to submit to the MW
                         api [default: <cpu-count>]
        --verbose        Print dots and stuff to note progress
        --debug          Print debug logging
"""
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from multiprocessing import cpu_count

import docopt
import mwapi
import mwapi.cli

from .util import dump_observation, read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger('requests').setLevel(logging.WARNING)
    host = args['--host']

    try_deleted_first = args['--deleted-1st']
    login = args['--login']

    if args['--input'] == "<stdin>":
        obs = read_observations(sys.stdin)
    else:
        obs = read_observations(open(args['--input']))

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(args['--output'], 'w')

    if args['--threads'] == "<cpu-count>":
        threads = cpu_count()
    else:
        threads = int(args['--threads'])

    verbose = args['--verbose']

    run(host, obs, try_deleted_first, login, output, threads, verbose)


def run(host, obs, try_deleted_first, login, output, threads, verbose):

    session = mwapi.Session(
        host,
        user_agent="Fetch text (wikigrammar) <ahalfaker@wikimedia.org>",
        formatversion=2)
    if login:
        mwapi.cli.do_login(session, host)

    obs_batches = read_chunks(obs, 10)
    fetcher = TextFetcher(
        session, try_deleted_first=try_deleted_first, login=login)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for obs_with_text in executor.map(fetcher.fetch_text, obs_batches):
            if verbose:
                sys.stderr.write(str(len(obs_with_text)) + " ")
                sys.stderr.flush()

            for ob in obs_with_text:
                dump_observation(ob, output)

        if verbose:
            sys.stderr.write("\n")


def read_chunks(iterable, size):
    while True:
        output = tuple(islice(iterable, size))
        if output:
            yield output
        else:
            break


class TextFetcher:

    def __init__(self, session, try_deleted_first=False, login=False):
        self.session = session
        if not login:
            self.attempts = [self._get_live_text]
        elif try_deleted_first:
            self.attempts = [self._get_deleted_text, self._get_live_text]
        else:
            self.attempts = [self._get_live_text, self._get_deleted_text]

    def fetch_text(self, obs):
        rev_ids = set(ob['rev_id'] for ob in obs)
        texts = {}
        for _get_text in self.attempts:
            text_map = _get_text(rev_ids - texts.keys())
            texts.update(text_map)

        return list(self.intersect(obs, texts))

    @classmethod
    def intersect(cls, obs, texts):
        for ob in obs:
            if ob['rev_id'] in texts:
                ob['text'] = texts[ob['rev_id']]
                yield ob

    def _get_live_text(self, rev_ids):
        if len(rev_ids) == 0:
            return {}
        doc = self.session.get(
            action='query',
            prop='revisions',
            revids=rev_ids,
            rvslots=['main'],
            rvprop={"content", "ids"}
        )
        return self._build_text_map(doc)

    def _get_deleted_text(self, rev_ids):
        if len(rev_ids) == 0:
            return {}

        doc = self.session.get(
            action='query',
            prop='deletedrevisions',
            revids=rev_ids,
            drvslots=['main'],
            drvprop={"content", "ids"}
        )

        return self._build_text_map(doc, revision_key='deletedrevisions')

    @staticmethod
    def _build_text_map(doc, revision_key='revisions'):
        text_map = {}
        for page_doc in doc['query'].get('pages', []):
            for rev_doc in page_doc.get(revision_key, []):
                if 'content' in rev_doc['slots']['main']:
                    text_map[rev_doc['revid']] = \
                        rev_doc['slots']['main']['content']

        return text_map
