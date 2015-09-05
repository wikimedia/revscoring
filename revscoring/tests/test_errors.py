import pickle
import traceback

from ..errors import (CaughtDependencyError, DependencyError, DependencyLoop,
                      MissingResource, RevisionNotFound)


def test_exceptions_picklability():
    de = DependencyError("FooBar")
    pickle.loads(pickle.dumps(de))

    try:
        assert False, "woops"
    except Exception as e:
        tb = traceback.extract_stack()
        cde = CaughtDependencyError("FooBar", e, tb)
        pickled_cde = pickle.dumps(cde)
        pickle.loads(pickled_cde)

    dl = DependencyLoop("FooBar")
    pickle.loads(pickle.dumps(dl))

    mr = MissingResource("FooBar")
    pickle.loads(pickle.dumps(mr))

    rnf = RevisionNotFound()
    pickle.loads(pickle.dumps(rnf))
