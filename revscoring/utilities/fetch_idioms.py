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
import re
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


def is_idiom(phrase):
    """
        Checks if a phrase meets certain criteria to make it an idiom
    """
    if re.match('Category:English|Citation:|Appendix:', phrase):
        return False
    # One word phrases
    if re.match(r"^[\w\-\']+$", phrase):
        return False
    # Two-worded phrases
    if re.match(r"^[\w\-\']+ [\w\-\']+$", phrase):
        return False
    # Similes
    if 'as a' in phrase:
        return False
    return True


def combine_words(first_word, following_words):
    """
        Combines the first word and following words into one regex
        Sample:
        first_word (word1|word2|...|wordx)
    """
    if len(following_words) == 1:
        idiom_regex = '{} {}'.format(
            first_word, "".join(following_words))
    else:
        idiom_regex = '{} ({})'.format(
            first_word, "|".join(following_words))
    if not idiom_regex.isspace():
        return idiom_regex


def create_regexes(idioms):
    """
        Creates regexes out of idioms
    """
    regexes = []
    first_word = ''
    following_words = []
    for idiom in idioms:
        words = idiom.split()
        if first_word == '':
            pass
        elif first_word == words[0]:
            following_words.append(" ".join(words[1:]))
            continue
        else:
            regex = combine_words(first_word, following_words)
            if regex:
                regexes.append(regex)
        first_word = words[0]
        following_words = [" ".join(words[1:])]

    regex = combine_words(first_word, following_words)
    if regex:
        regexes.append(regex)

    return regexes


def fetch():
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
            phrase = page_doc['title']
            if not is_idiom(phrase):
                continue
            idioms.append(phrase)

    regexes = create_regexes(idioms)
    return regexes


def run(output, verbose):
    logger = logging.getLogger(__name__)
    if verbose:
        logger.info('Fetching idioms...')

    regexes = fetch()
    for regex in regexes:
        dump_observation(regex, output)
