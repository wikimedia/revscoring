"""
``revscoring features -h``
::

    Tool for reading and parsing "*.w_cache.*" files, observations and features.

    Usage:
        features -h | --help
        features [--input=<path>]
                 [--limit=<integer>]

    Options:
        -h --help               Print this documentation
        --input=<path>          Path to a file containing rev_id-label pairs
                                [default: <stdin>]
        --limit=<integer>       Maximum number of observations to show, or 0 for no limit.
                                [default: 0]
"""
import sys

import docopt
import yaml

from .util import read_observations


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    if args['--input'] == "<stdin>":
        in_stream = sys.stdin
    else:
        in_stream = open(args['--input'])

    limit = int(args['--limit'])

    run(in_stream, limit)


def run(in_stream, limit):
    observations = read_observations(in_stream)
    observations = list(observations)
    if limit > 0:
        observations = observations[:limit]

    print(yaml.safe_dump(observations))
