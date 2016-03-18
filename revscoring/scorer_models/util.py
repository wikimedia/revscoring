import json
import random
from collections import defaultdict

import numpy


def normalize(v):
    if isinstance(v, numpy.bool_):
        return bool(v)
    elif isinstance(v, numpy.float):
        return float(v)
    elif isinstance(v, tuple):
        return list(v)
    else:
        return v


def key_normalize(v):
    v = normalize(v)
    if isinstance(v, bool) or isinstance(v, int) or isinstance(v, float) or \
       isinstance(v, str):
        return v
    elif isinstance(v, list) or isinstance(v, dict):
        return json.dumps(v)
    else:
        return str(v)


def normalize_json(doc):
    if isinstance(doc, dict):
        return {key_normalize(k): normalize_json(v)
                for k, v in doc.items()}
    elif isinstance(doc, list) or isinstance(doc, tuple):
        return [normalize_json(v) for v in doc]
    else:
        return normalize(doc)


def format_params(doc):
    if doc is None:
        return None
    else:
        return ", ".join("{0}={1}".format(k, json.dumps(v))
                         for k, v in doc.items())


def balance_weights(labels):
    """
    Generates a mapping of class weights that will re-weight a training set
    in a balanced way such that weight(label) = len(obs) / freq(label in obs).
    """
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1

    return {l: (len(labels) / counts[l]) for l in counts}


def balance_sample_weights(labels):
    """
    Generates a vector of balancing weights for a vector of labels
    """
    weights = balance_weights(labels)
    return [weights[label] for label in labels]


def balance_sample(values_labels):
    """
    Rebalances a set of a labels based on the label with the most
    observations by sampling (with replacement[1]) from lesser labels.
    For example, the following dataset has unbalanced observations:
        (0.10  0.20  0.30),  True
        (0.20  0.10  0.30),  False
        (0.10  0.15  0.40),  True
        (0.09  0.40  0.30),  False
        (0.15  0.00  0.28),  True
    True` occurs three times while `False` only occurs twice.  This
    function would randomly choose one of the False observations to
    duplicate in order to balance the labels.  For example:
        (0.10  0.20  0.30),  True
        (0.20  0.10  0.30),  False
        (0.20  0.10  0.30),  False
        (0.10  0.15  0.40),  True
        (0.09  0.40  0.30),  False
        (0.15  0.00  0.28),  True
    Why would anyone want to do this?  If you don't, SVM's
    predict_proba() will return values that don't represent it's
    predictions.  This is a hack.  It seems to work in practice with large
    numbers of observations[2].
    1. See https://www.ma.utexas.edu/users/parker/sampling/repl.htm for a
       discussion of "sampling with replacement".
    2. http://nbviewer.ipython.org/github/halfak/
        Objective-Revision-Evaluation-Service/blob/ipython/ipython/
        Wat%20predict_proba.ipynb
    """
    # Group observations by label
    groups = defaultdict(list)
    for feature_values, label in values_labels:
        groups[label].append((feature_values, label))

    # Find out which label occurs most often and how often
    max_label_count = max(len(groups[label]) for label in groups)

    # Resample the max observations from each group of observations.
    new_feature_values = []
    for label in groups:
        # Add back all of the labels we have
        new_feature_values.extend(groups[label])

        # Supplement with sampling
        additional_obs = max_label_count - len(groups[label])
        new_feature_values.extend(random.choice(groups[label])
                                  for i in range(additional_obs))

    # Shuffle the observations again before returning.
    random.shuffle(new_feature_values)
    return new_feature_values
