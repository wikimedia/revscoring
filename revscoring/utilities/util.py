import base64
import json
import logging
import os
import pickle
import random
import signal
from collections import OrderedDict

import yamlconf

logger = logging.getLogger(__name__)

DECODERS = {
    'int': lambda v: int(v),
    'float': lambda v: float(v),
    'str': lambda v: str(v),
    'bool': lambda v: v in ("True", "true", "1", "T", "y", "Y")
}


def read_observations(f):
    for line in f:
        observation = json.loads(line)
        if 'cache' in observation:
            observation['cache'] = pickle.loads(
                base64.b85decode(bytes(observation['cache'], 'ascii')))

        yield observation


def dump_observation(observation, f):
    if 'cache' in observation:
        observation['cache'] = \
            str(base64.b85encode(pickle.dumps(observation['cache'])), 'ascii')

    json.dump(observation, f)
    f.write("\n")


def read_labels_and_population_rates(labels_str, label_weights_strs,
                                     pop_rates_strs, config_path):
    # First try config file
    if config_path:
        labels_config = yamlconf.load(open(os.path.expanduser(config_path)))
        return read_labels_config(labels_config)

    # Try to read --labels
    if labels_str is not None:
        labels = [json.loads(l) for l in labels_str.strip().split(",")]
    else:
        labels = None

    # Try to read --label-weight
    if len(label_weights_strs) > 0:
        label_weights = OrderedDict()
        for label_weights_str in label_weights_strs:
            label, weight = (
                json.loads(s) for s in label_weights_str.split("=", 1))
            label_weights[label] = weight
    else:
        label_weights = None

    # Try to read --pop-rate
    if len(pop_rates_strs) == 0:
        population_rates = None
    else:
        population_rates = OrderedDict()
        for label_rate_str in pop_rates_strs:
            label, rate = (json.loads(s) for s in label_rate_str.split("=", 1))
            population_rates[label] = rate

    if labels is None and label_weights is None and population_rates is None:
        raise RuntimeError("Either --pop-rates or --labels or \
                           --labels-config must be specified")
    elif labels is None:
        if population_rates is not None:
            labels = list(population_rates.keys())
        else:
            labels = list(label_weights.keys())

    return labels, label_weights, population_rates


def read_labels_config(labels_config):
    labels = []
    label_weights = {}
    population_rates = {}
    for label_doc in labels_config['labels']:
        label = label_doc['value']
        labels.append(label)
        if 'weight' in label_doc:
            label_weights[label] = label_doc['weight']
        if 'population_rate' in label_doc:
            population_rates[label] = label_doc['population_rate']

    return labels, label_weights, population_rates


def train_test_split(observations, test_prop=0.25):
    # Split train and test set from obs.
    observations = list(observations)
    random.shuffle(observations)

    test_set_size = int(len(observations) * test_prop)

    test_set = observations[:test_set_size]
    train_set = observations[test_set_size:]

    return train_set, test_set


class Timeout:
    """
    A context for performing a timeout.
    """

    def __init__(self, timeout_seconds):
        self.timeout_seconds = int(timeout_seconds)

    def handle_timeout(self, signum, frame):
        raise RuntimeError("Execution timed out at {0} seconds."
                           .format(self.timeout_seconds))

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.timeout_seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
