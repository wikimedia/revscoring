import json
import random
from io import BytesIO
from itertools import chain

from nose.tools import eq_

from ...features import Feature
from ...languages import Language
from ..scorer import MLScorerModel
from ..svc import LinearSVCModel, RBFSVCModel, SVCModel


def process_float(): return float()
some_float = Feature("some_float", process_float(),
                      depends_on=[], returns=float)

def process_other_float(): return float()
other_float = Feature("other_float", process_other_float(),
                      depends_on=[], returns=float)
FEATURES = [some_float, other_float]


def is_badword(word): return word == "badword"
def is_misspelled(word): return word == "misspelled"
some_language = Language(is_badword, is_misspelled)
LANGUAGE = some_language

def train_score(model):
    deterministic = random.Random(0)
    observations = list(chain(
        zip(((some, other) for some, other in
             zip((deterministic.normalvariate(1, .3) for i in range(200)),
                 (deterministic.normalvariate(2, .5) for i in range(200)))),
            (True for i in range(200))),
        zip(((some, other) for some, other in
             zip((deterministic.normalvariate(-1, .5) for i in range(35)),
                 (deterministic.normalvariate(-2, .3) for i in range(35)))),
            (False for i in range(35)))
    ))
    deterministic.shuffle(observations)
    
    mid = int(len(observations)/2)
    train_set = observations[:mid]
    test_set = observations[mid:]
    
    model.train(train_set)
    score_doc = next(model.score([(-1,-2)]))
    
    eq_(score_doc['prediction'], False)
    json.dumps(score_doc) # Checks if the doc is JSONable
    
    test_stats = model.test(test_set)
    
    del test_stats['roc']
    print(test_stats)
    assert test_stats['auc'] > 0.5

def pickle_and_unpickle(model):
    f = BytesIO()
    model.dump(f)
    f.seek(0) # Rewind the file
    reconstructed_model = MLScorerModel.load(f)
    eq_([f.name for f in reconstructed_model.features],
        [f.name for f in model.features])
    eq_(type(reconstructed_model), type(model))

def test_svc():
    model = SVCModel(FEATURES, LANGUAGE)
    train_score(model)
    pickle_and_unpickle(model)
    
def test_linear_svc():
    model = LinearSVCModel(FEATURES, LANGUAGE)
    train_score(model)
    pickle_and_unpickle(model)
    
def test_rbf_svc():
    model = RBFSVCModel(FEATURES, LANGUAGE)
    train_score(model)
    pickle_and_unpickle(model)
