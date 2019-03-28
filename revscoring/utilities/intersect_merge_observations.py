"""
``revscoring intersect_merge_observations -h``
::

    Intersect observation data.  Fields will be merged.  Data is triaged
    according to the order of filenames in the commandline arguments,
    with the later files taking preference over earlier.

    Usage:
        intersect_merge_observations -h | --help
        intersect_merge_observations <input>...
            [--output=<path>]
            [--id-column=<str>]

    Options:
        <input>           List of input file paths
        --output=<path>   Path to write out the merged observations
                          [default: <stdout>]
        --id-column=<str> Name of the id column for deduplication.
                          [default: rev_id]
"""

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

    observation_sets = (read_observations(open(path, "r"))
                        for path in args['<input>'])

    intersected_observations = intersect_merge_observations(
        observation_sets, id_column=args['--id-column'])

    for ob in intersected_observations:
        dump_observation(ob, out_file)


def intersect_merge_observations(observation_sets, id_column):
    """Intersect all observations, returning the output as an iterable.
    """
    observation_maps = [
        {ob[id_column]: ob for ob in observation_set}
        for observation_set in observation_sets]

    for id_ in observation_maps[0]:
        # Key exists in all sets
        if sum(id_ in om for om in observation_maps) == len(observation_maps):
            new_ob = {}
            for observation_map in observation_maps:
                new_ob = deep_merge.merge(new_ob, observation_map[id_])

            yield new_ob
