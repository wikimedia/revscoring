"""
``revscoring extract_features -h``
::

    Adds features to a set of labeled revisions.

    Reads a TSV file of <rev_id>\t<label> pairs and replaces the
    <rev_id> field with the extracted feature values.

    Input: <rev_id>[TAB]<label>

    Output: <feature_1>[TAB]<feature_2>[TAB]...[TAB]<label>


    Usage:
        extract_features -h | --help
        extract_features <features> --host=<url> [--rev-labels=<path>]
                                                 [--value-labels=<path>]
                                                 [--include-revid]
                                                 [--extractors=<num>]
                                                 [--login]
                                                 [--profile=<path>]
                                                 [--verbose] [--debug]

    Options:
        -h --help               Print this documentation
        <features>              Classpath to a list/tuple of features
        --host=<url>            The url pointing to a MediaWiki API to use
                                for extracting features
        --rev-labels=<path>     Path to a file containing rev_id-label pairs
                                [default: <stdin>]
        --value-labels=<path>   Path to a file to write feature-labels to
                                [default: <stdout>]
        --include-revid         If set, include the revision ID as the first
                                column in the output TSV
        --extractors=<num>      The number of extractors to run in parallel
                                [default: <cpu count>]
        --login                 If set, prompt for username and password
        --profile=<path>        Path to a file to write extraction profiling
                                output
        --verbose               Print dots and stuff
        --debug                 Print debug logging
"""
import getpass
import logging
import sys
import time
from multiprocessing import Pool, cpu_count
from statistics import mean, median

import docopt
import mwapi
import yamlconf
from tabulate import tabulate

from ..errors import CommentDeleted, RevisionNotFound, TextDeleted, UserDeleted
from ..extractors import api
from .util import encode

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    features = yamlconf.import_module(args['<features>'])

    session = mwapi.Session(args['--host'],
                            user_agent="Revscoring feature extractor utility")
    if args['--login']:
        sys.stderr.write("Log into " + args['--host'] + "\n")
        sys.stderr.write("Username: ")
        sys.stderr.flush()
        username = open('/dev/tty').readline().strip()
        password = getpass.getpass("Password: ")
        session.login(username, password)
    extractor = api.Extractor(session)

    if args['--rev-labels'] == "<stdin>":
        rev_labels = read_rev_labels(sys.stdin)
    else:
        rev_labels = read_rev_labels(open(args['--rev-labels']))

    if args['--value-labels'] == "<stdout>":
        value_labels = sys.stdout
    else:
        value_labels = open(args['--value-labels'], 'w')

    include_revid = bool(args['--include-revid'])

    if args['--extractors'] == "<cpu count>":
        extractors = cpu_count()
    else:
        extractors = int(args['--extractors'])

    if args['--profile'] is not None:
        profile_f = open(args['--profile'], 'w')
    else:
        profile_f = None

    verbose = args['--verbose']
    debug = args['--debug']

    run(rev_labels, value_labels, features, extractor, include_revid,
        extractors, profile_f, verbose, debug)


def read_rev_labels(f):
    # Check if first line is a header
    rev_id, label = f.readline().strip().split("\t")
    if rev_id != "rev_id":
        yield int(rev_id), label

    for line in f:
        rev_id, label = line.strip().split('\t')
        yield int(rev_id), label


def run(rev_labels, value_labels, features, extractor, include_revid,
        extractors, profile_f, verbose, debug):
    logging.basicConfig(
        level=logging.WARNING if not debug else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    extractor_context = ConfiguredExtractor(extractor, features)
    extractor_pool = Pool(processes=extractors)

    results = extractor_pool.imap(extractor_context.extract, rev_labels)
    combined_profile = {}
    extraction_durations = []

    for e, rev_id, label, feature_values, profile, duration in results:
        if isinstance(e, RevisionNotFound):
            if verbose:
                sys.stderr.write("?")
                sys.stderr.flush()
        elif isinstance(e, TextDeleted) or isinstance(e, UserDeleted) or \
             isinstance(e, CommentDeleted):
            if verbose:
                sys.stderr.write("d")
                sys.stderr.flush()
        elif e is not None:
            logger.error("An error occured while processing {0}:"
                         .format(rev_id))
            logger.error("\t{0}: {1}".format(e.__class__.__name__, str(e)))
        else:
            # Append extraction duraton
            extraction_durations.append(duration)

            # Update profile
            for dependent, durations in profile.items():
                if dependent in combined_profile:
                    combined_profile[dependent].extend(durations)
                else:
                    combined_profile[dependent] = durations

            # Emit feature values
            fields = list(feature_values) + [label]

            if include_revid:
                fields = [rev_id] + fields

            value_labels.write("\t".join(encode(v)
                                         for v in fields))
            value_labels.write("\n")

            if verbose:
                sys.stderr.write(".")
                sys.stderr.flush()

    if verbose:
        sys.stderr.write("\n")

    if profile_f is not None:
        write_profile(profile_f, features, extraction_durations,
                      combined_profile)


class ConfiguredExtractor:

    def __init__(self, extractor, features):
        self.extractor = extractor
        self.features = features

    def extract(self, rev_label):
        rev_id, label = rev_label
        profile = {}
        try:
            start = time.time()
            feature_values = \
                list(self.extractor.extract(rev_id, self.features,
                                            profile=profile))
            duration = time.time() - start
            error = None
        except Exception as e:
            feature_values = None
            duration = None
            error = e

        profile = {str(d): s for d, s in profile.items()}
        return error, rev_id, label, feature_values, profile, duration


def write_profile(profile_f, features, extraction_durations, combined_profile):
    profile_f.write("Extracting {0} features\n\n".format(len(features)))
    table = tabulate(
        [('extractions', len(extraction_durations)),
         ('total_time', round(sum(extraction_durations), 3)),
         ('min_time', round(min(extraction_durations), 3)),
         ('max_time', round(max(extraction_durations), 3)),
         ('mean_time', round(mean(extraction_durations), 3)),
         ('median_time', round(median(extraction_durations), 3))],
        headers=["stat", "value"],
        tablefmt="pipe"
    )
    profile_f.write(table + "\n")
    profile_f.write("\n")

    feature_profiles = []
    datasource_profiles = []
    misc_profiles = []
    for dependent_name, durations in combined_profile.items():
        row = (dependent_name.replace("<", "\<").replace(">", "\>"),
               len(durations),
               round(min(durations), 3),
               round(max(durations), 3),
               round(mean(durations), 3),
               round(median(durations), 3))
        if "feature." in dependent_name:
            feature_profiles.append(row)
        elif "datasource." in dependent_name:
            datasource_profiles.append(row)
        else:
            misc_profiles.append(row)

    profile_f.write("# Features\n")
    write_dependent_profiles(profile_f, feature_profiles)

    profile_f.write("# Datasources\n")
    write_dependent_profiles(profile_f, datasource_profiles)

    profile_f.write("# Misc\n")
    write_dependent_profiles(profile_f, misc_profiles)


def write_dependent_profiles(profile_f, dependent_profiles):
    if len(dependent_profiles) > 0:
        dependent_profiles.sort(key=lambda row: row[4], reverse=True)
        table = tabulate(
            dependent_profiles[1:25],
            headers=["name", "executions", "min", "max", "mean", "median"],
            tablefmt="pipe"
        )
        profile_f.write(table + "\n")
        profile_f.write("\n")
