import pickle
import traceback

from nose.tools import eq_

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
    eq_(str(dl), "DependencyLoop: FooBar")

    mr = MissingResource("FooBar")
    pickle.loads(pickle.dumps(mr))
    eq_(str(mr), "MissingResource: FooBar")

    rnf = RevisionNotFound(DependentSet("revision"), 10)
    pickle.loads(pickle.dumps(rnf))
    eq_(str(rnf), "RevisionNotFound: Could not find revision ({revision}:10)")

    pnf = PageNotFound(DependentSet("page"), 12)
    pickle.loads(pickle.dumps(pnf))
    eq_(str(pnf), "PageNotFound: Could not find page ({page}:12)")

    unf = UserNotFound(DependentSet("user"), 10)
    pickle.loads(pickle.dumps(unf))
    eq_(str(unf), "UserNotFound: Could not find user account ({user}:10)")

    ud = UserDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(ud))
    eq_(str(ud), "UserDeleted: User deleted ({revision})")

    cd = CommentDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(cd))
    eq_(str(cd), "CommentDeleted: Comment deleted ({revision})")

    td = TextDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(td))
    eq_(str(td), "TextDeleted: Text deleted ({revision})")

    cde = CaughtDependencyError("Test", RuntimeError("Foo"))
    pickle.loads(pickle.dumps(cde))
    eq_(str(cde), "RuntimeError: Test\nNone")
