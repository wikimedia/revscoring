"""
``revscoring extract -h``
::

    Extracts a list of `dependent` for a set of revisions.

    Reads file containing revision observations, extracts dependents
    (Features and Datasources), and writes extended observations out for future
    use.

    Usage:
        extract -h | --help
        extract <dependent>... --host=<url> [--input=<path>]
                                            [--output=<path>]
                                            [--extractors=<num>]
                                            [--batch-size=<num>]
                                            [--login]
                                            [--profile=<path>]
                                            [--verbose] [--debug]

    Options:
        -h --help               Print this documentation
        <dependent>             Classpath to a dependent or a list of
                                dependents
        --host=<url>            The url pointing to a MediaWiki API to use
                                for extracting features
        --input=<path>          Path to a file containing rev_id-label pairs
                                [default: <stdin>]
        --output=<path>         Path to a file to write extracted data to
                                [default: <stdout>]
        --extractors=<num>      The number of extractors to run in parallel
                                [default: <cpu count>]
        --batch-size=<num>      The number of rev_ids to batch together per
                                request to the API [default: 50]
        --login                 If set, prompt for username and password
        --profile=<path>        Path to a file to write extraction profiling
                                output
        --verbose               Print dots and stuff
        --debug                 Print debug logging
"""
import logging
import sys
import time
from itertools import islice
from multiprocessing import Pool, cpu_count
from statistics import mean, median

import docopt
import mwapi
import yamlconf
from tabulate import tabulate

from ..dependencies import Dependent
from ..errors import CommentDeleted, RevisionNotFound, TextDeleted, UserDeleted
from ..extractors import api
from .util import dump_observation, get_user_pass, read_observations

logger = logging.getLogger(__name__)


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    logging.basicConfig(
        level=logging.WARNING if not args['--debug'] else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    dependents = []
    for dependent_path in args['<dependent>']:
        dependent_or_list = yamlconf.import_path(dependent_path)
        if isinstance(dependent_or_list, Dependent):
            dependents.append(dependent_or_list)
        else:
            dependents.extend(dependent_or_list)

    session = mwapi.Session(args['--host'],
                            user_agent="Revscoring extract utility")
    if args['--login']:
        username, password = get_user_pass(args['--host'])
        session.login(username, password)
    extractor = api.Extractor(session)

    if args['--input'] == "<stdin>":
        observations = read_observations(sys.stdin)
    else:
        observations = read_observations(open(args['--input']))

    if args['--output'] == "<stdout>":
        output = sys.stdout
    else:
        output = open(args['--output'], 'w')

    if args['--extractors'] == "<cpu count>":
        extractors = cpu_count()
    else:
        extractors = int(args['--extractors'])

    batch_size = int(args['--batch-size'])

    if args['--profile'] is not None:
        profile_f = open(args['--profile'], 'w')
    else:
        profile_f = None

    verbose = args['--verbose']
    debug = args['--debug']

    run(observations, output, dependents, extractor, extractors, batch_size,
        profile_f, verbose, debug)


def run(observations, output, dependents, extractor, extractors, batch_size,
        profile_f, verbose, debug):
    logging.basicConfig(
        level=logging.WARNING if not debug else logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s -- %(message)s'
    )

    profile = {}
    results = extract(dependents, observations, extractor,
                      extractors=extractors,
                      batch_size=batch_size, profile=profile)

    for e, observation in results:
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
                         .format(observation['rev_id']))
            logger.error("\t{0}: {1}".format(e.__class__.__name__, str(e)))
        else:
            dump_observation(observation, output)

            if verbose:
                sys.stderr.write(".")
                sys.stderr.flush()

    if verbose:
        sys.stderr.write("\n")

    if profile_f is not None:
        write_profile(profile_f, dependents, profile, batch_size)


def extract(dependents, observations, extractor, extractors="<cpu count>",
            batch_size=50, profile=None):

    extractor_context = ConfiguredExtractor(extractor, dependents)
    extractor_pool = Pool(processes=extractors)

    observation_batches = batch(observations, batch_size)

    result_batches = extractor_pool.imap(
        extractor_context.extract, observation_batches)

    combined_profile = profile if profile is not None else {}
    combined_profile['per_batch_duration'] = []

    for results, batch_profile, batch_duration in result_batches:
        if len(results) == batch_size:
            combined_profile['per_batch_duration'].append(batch_duration)
        else:
            combined_profile['per_batch_duration'].append(
                batch_duration / (len(results) / batch_size))
        combine_profiles(combined_profile, batch_profile)
        yield from results


def batch(iterable, size):
    while True:
        batch = list(islice(iterable, 0, size))
        if len(batch) > 0:
            yield batch
        else:
            break


def combine_profiles(profile, new_profile):
    for stat, vals in new_profile.items():
        if stat in profile:
            profile[stat].extend(vals)
        else:
            profile[stat] = vals


class ConfiguredExtractor:

    def __init__(self, extractor, dependents):
        self.extractor = extractor
        self.dependents = dependents

    def extract(self, observations):
        rev_ids = [ob['rev_id'] for ob in observations]
        profile = {}
        caches = {ob['rev_id']: ob['cache'] for ob in observations
                                            if 'cache' in ob}
        start = time.time()
        extractions = self.extractor.extract(
            rev_ids, self.dependents, caches=caches, profile=profile)
        results = []
        for observation, (e, values) in zip(observations, extractions):
            if e is None:
                # update observation['cache']
                observation['cache'] = observation.get('cache', {})
                for dependent, value in zip(self.dependents, values):
                    observation['cache'][str(dependent)] = value

            results.append((e, observation))

        duration = time.time() - start
        profile = {str(d): s for d, s in profile.items()}
        return results, profile, duration


def write_profile(profile_f, dependents, profile, batch_size):
    profile_f.write("Extracting {0} values:\n".format(len(dependents)))
    for dependent in dependents:
        profile_f.write("* `{0}`\n".format(dependent))

    profile_f.write("\n".format(batch_size))
    profile_f.write("Batch size: {0}\n\n".format(batch_size))

    table = tabulate(
        [('batch_extractions', len(profile['per_batch_duration'])),
         ('total_time', round(sum(profile['per_batch_duration']), 3)),
         ('min_time', round(min(profile['per_batch_duration']), 3)),
         ('max_time', round(max(profile['per_batch_duration']), 3)),
         ('mean_time', round(mean(profile['per_batch_duration']), 3)),
         ('median_time', round(median(profile['per_batch_duration']), 3))],
        headers=["stat", "value"],
        tablefmt="pipe"
    )
    profile_f.write(table + "\n\n")
    del profile['per_batch_duration']

    feature_profiles = []
    datasource_profiles = []
    misc_profiles = []
    for dependent_name, durations in profile.items():
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

    if len(feature_profiles) > 0:
        profile_f.write("# Features\n")
        write_dependent_profiles(profile_f, feature_profiles)

    if len(datasource_profiles) > 0:
        profile_f.write("# Datasources\n")
        write_dependent_profiles(profile_f, datasource_profiles)

    if len(misc_profiles) > 0:
        profile_f.write("# Misc\n")
        write_dependent_profiles(profile_f, misc_profiles)


def write_dependent_profiles(profile_f, dependent_profiles):
    if len(dependent_profiles) > 0:
        dependent_profiles.sort(key=lambda row: row[4], reverse=True)
        table = tabulate(
            dependent_profiles[0:25],
            headers=["name", "executions", "min", "max", "mean", "median"],
            tablefmt="pipe"
        )
        profile_f.write(table + "\n")
        profile_f.write("\n")
