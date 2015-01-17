from io import BytesIO
from revscoring.scorers import MLScorerModel
from nose.tools import eq_

from ...features import (proportion_of_badwords_added,
                         proportion_of_symbolic_added)
from ..linear_svc import LinearSVC

def test_model():
    model = LinearSVC.MODEL([proportion_of_badwords_added,
                             proportion_of_symbolic_added])
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
    
    f = BytesIO()
    model.dump(f)
    f.seek(0)
    model = LinearSVC.MODEL.load(f)

    def test_serialization():
        model = LinearSVC.MODEL([proportion_of_badwords_added,
                                 proportion_of_symbolic_added])
        f = BytesIO() # open("/tmp/aksjbdkasbdka", 'wb')
        model.dump(f)
        f.seek(0) # Rewind the file
        reconstructed_model = MLScorerModel.load(f)
        eq_(reconstructed_model.features, model.features)
        eq_(type(reconstructed_model), type(model))