"""
``revscoring fetch_idioms -h``
::

    Gets a list of English language idioms from en.wiktionary.org.

    Usage:
        fetch_idioms [--output=<path>]
                   [--verbose] [--debug]

    Options:
        -h --help        Print this documentation
        --output=<path>  Path to a file to write the idioms
                         [default: <stdout>]
        --verbose        Print dots and stuff to note progress
        --debug          Print debug logging
"""

import logging
import sys

import docopt
import mwapi

from .util import dump_observation


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.INFO if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )
    logging.getLogger('requests').setLevel(logging.WARNING)

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(args['--output'], 'w')

    verbose = args['--verbose']

    run(output, verbose)


def fetch(output):
    session = mwapi.Session("https://en.wiktionary.org")

    results = session.get(
        action='query',
        list='categorymembers',
        cmtitle="Category:English idioms",
        formatversion=2,
        continuation=True)

    idioms = []
    for doc in results:
        for page_doc in doc['query']['categorymembers']:
            # Some values take the form:
            # Category:English <variable>
            # For example: Category:English rhetorical questions
            # They are not idioms and should be filtered
            idiom = page_doc['title']
            if 'Category:English' not in idiom:
                idioms.append(idiom)

    for idiom in idioms:
        dump_observation(idiom, output)


def run(output, verbose):
    logger = logging.getLogger(__name__)
    if verbose:
        logger.info('Fetching idioms...')
    fetch(output)
