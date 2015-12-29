import pickle
import traceback

from ..dependencies import DependentSet
from ..errors import (CaughtDependencyError, CommentDeleted, DependencyError,
                      DependencyLoop, MissingResource, PageNotFound,
                      RevisionNotFound, TextDeleted, UserDeleted, UserNotFound)


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

    rnf = RevisionNotFound(DependentSet("revision"), 10)
    pickle.loads(pickle.dumps(rnf))

    pnf = PageNotFound(DependentSet("page"), 12)
    pickle.loads(pickle.dumps(pnf))

    unf = UserNotFound(DependentSet("user"), 10)
    pickle.loads(pickle.dumps(unf))

    ud = UserDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(ud))

    cd = CommentDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(cd))

    td = TextDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(td))
