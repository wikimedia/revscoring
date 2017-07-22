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
                          [default: "rev_id"]
"""

import docopt
import json
import sys

from .util import read_observations, dump_observation


def main(argv = None):
    args = docopt.docopt(__doc__, argv = argv)

    if args['--output'] == "<stdout>":
        out_file = sys.stdout
    else:
        out_file = open(args['--output'], "w")

    transformation = DataUnion(id_column = args['--id-column'])
    transformation.union(args['<input>'], out_file)


class DataUnion(object):

    # FIXME: This doubled default is annoying.
    def __init__(self, id_column = "rev_id"):
        self.id_column = id_column

        self.rev_objs = {}

    def read_file(self, in_file):
        lines = read_observations(in_file)
        for obj in lines:
            obj_id = obj[self.id_column]
            if obj_id not in self.rev_objs:
                self.rev_objs[obj_id] = []
            self.rev_objs[obj_id].append(obj)

    def union(self, in_paths, out_file):

        for index, path in enumerate(in_paths):
            with open(path, "r") as file_obj:
                self.read_file(file_obj)

        for obj_id, objs in self.rev_objs.items():
            merged = {}

            for obj in objs:
                merged.update(obj)

            dump_observation(merged, out_file)
