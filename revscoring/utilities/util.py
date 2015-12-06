import random
import signal


def encode(val, none_val="NULL"):
    if val is None:
        return none_val
    elif isinstance(val, bytes):
        val = str(val, 'utf-8', "replace")
    else:
        val = str(val)

    return val.replace("\t", "\\t").replace("\n", "\\n")


DECODERS = {
    'int': lambda v: int(v),
    'float': lambda v: float(v),
    'str': lambda v: str(v),
    'bool': lambda v: v in ("True", "true", "1", "T", "y", "Y")
}


def read_observations(f, features, decode_label):
    for line in f:
        parts = line.strip().split("\t")
        values = parts[:-1]
        label = parts[-1]

        label = decode_label(label)

        feature_values = []
        for feature, value in zip(features, values):

            if feature.returns == bool:
                feature_values.append(value == "True")
            else:
                feature_values.append(feature.returns(value))

        yield feature_values, label


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
