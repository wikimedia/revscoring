import pickle


from ..datasource import Datasource


def check_datasource(ds):
    assert isinstance(ds, Datasource)
    assert pickle.loads(pickle.dumps(ds)) == ds
