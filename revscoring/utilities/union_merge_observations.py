"""
``revscoring union_merge_observations -h``
::

    Merge labeled revisions, taking the union of values for any rows with
    the same id.  Data is triaged according to the order of filenames in the
    commandline arguments, with the later files taking preference over earlier.
    Behavior is not specified if an input file has duplicate revisions within
    it.

    FIXME: Reading everything into memory is reckless.  Estimate where this
    hits a wall.

    Usage:
        union_merge_observations -h | --help
        union_merge_observations <input>...
            [--output=<path>]
            [--id-column=<str>]

    Options:
        <input>           List of input file paths
        --output=<path>   Path to write out the merged observations
                          [default: <stdout>]
        --id-column=<str> Name of the id column for deduplication.
                          [default: rev_id]
"""

import collections
import docopt
import sys

from .util import read_observations, dump_observation


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    if args['--output'] == "<stdout>":
        out_file = sys.stdout
    else:
        out_file = open(args['--output'], "w")

    observations = []
    for path in args['<input>']:
        with open(path, "r") as in_file:
            observations.extend(read_observations(in_file))

    merged_observations = union_merge(observations,
                                        id_column=args['--id-column'])
    for ob in merged_observations:
        dump_observation(ob, out_file)


def union_merge(observations, id_column):

    id_map = collections.defaultdict(dict)
    for ob in observations:
        # Get the id value.
        ob_id = ob[id_column]
        id_map[ob_id].update(ob)

    return id_map.values()
