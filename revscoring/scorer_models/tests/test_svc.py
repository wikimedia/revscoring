from ..svc import SVCModel, LinearSVCModel, RBFSVCModel
from .util import FEATURES, train_score, pickle_and_unpickle

def test_svc():
    model = SVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
    
def test_linear_svc():
    model = LinearSVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
    
def test_rbf_svc():
    model = RBFSVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
