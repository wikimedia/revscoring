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
        --id-column=<str> Name of the id field for deduplication.
                          [default: rev_id]
"""

import collections
import itertools
import sys

import deep_merge
import docopt

from .util import dump_observation, read_observations


def main(argv=None):
    """Parse commandline parameters, read files and write merged data.
    """
    args = docopt.docopt(__doc__, argv=argv)

    if args['--output'] == "<stdout>":
        out_file = sys.stdout
    else:
        out_file = open(args['--output'], "w")

    observation_chunks = (read_observations(open(path, "r"))
                          for path in args['<input>'])
    all_observations = itertools.chain(*observation_chunks)

    merged_observations = union_merge_observations(
        all_observations, id_column=args['--id-column'])
    for ob in merged_observations:
        dump_observation(ob, out_file)


def union_merge_observations(observations, id_column):
    """Merge all observations, returning the output as a list.
    """
    id_map = collections.defaultdict(dict)
    for ob in observations:
        # Get the id value.
        ob_id = ob[id_column]

        # Merge the contents, with later entries taking precedence when keys
        # match.
        id_map[ob_id] = deep_merge.merge(id_map[ob_id], ob)

    return id_map.values()
