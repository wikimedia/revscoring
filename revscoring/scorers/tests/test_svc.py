from io import BytesIO

from nose.tools import eq_

from ...features import (proportion_of_badwords_added,
                         proportion_of_symbolic_added)
from ..scorer import MLScorerModel
from ..svc import LinearSVC, RBFSVC, SVC


def train_score(model):
    train_stats = model.train([
        ([10.1, 20.1], True),
        ([19.2, 15.3], True),
        ([13.1, 12.5], True),
        ([0.5, 0.6], False),
        ([2.4, 0.1], False),
        ([0.9, 3.1], False)
    ])
    
    score_doc = next(model.score([[0.5,1.0]]))
    eq_(score_doc['prediction'], False)
    
    test_stats = model.test([
        ([13.1, 12.1], True),
        ([9.2, 19.3], True),
        ([12.1, 14.5], True),
        ([19.5, 19.6], False),
        ([2.4, 2.1], False),
        ([0.1, 3.1], False)
    ])
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
    model = SVC.MODEL([proportion_of_badwords_added,
                       proportion_of_symbolic_added])
    train_score(model)
    pickle_and_unpickle(model)
    
def test_linear_svc():
    model = LinearSVC.MODEL([proportion_of_badwords_added,
                             proportion_of_symbolic_added])
    train_score(model)
    pickle_and_unpickle(model)
    
def test_rbf_svc():
    model = RBFSVC.MODEL([proportion_of_badwords_added,
                       proportion_of_symbolic_added])
    train_score(model)
    pickle_and_unpickle(model)
