import pickle
import traceback

from revscoring.dependencies import Dependent, DependentSet
from revscoring.errors import (CaughtDependencyError, CommentDeleted,
                               DependencyError, DependencyLoop,
                               MissingResource, PageNotFound,
                               QueryNotSupported, RevisionNotFound,
                               TextDeleted, UserDeleted, UserNotFound,
                               UnexpectedContentType)


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
    assert str(dl) == "DependencyLoop: FooBar"

    mr = MissingResource("FooBar")
    pickle.loads(pickle.dumps(mr))
    assert str(mr) == "MissingResource: FooBar"

    qns = QueryNotSupported(
        Dependent("revision.page.suggested.properties"),
        "Unrecognized value for parameter \"action\": wbsgetsuggestions.")
    pickle.loads(pickle.dumps(qns))
    assert str(qns) == (
        "QueryNotSupported: Query failed " +
        "(dependent.revision.page.suggested.properties:Unrecognized value for " +
        "parameter \"action\": wbsgetsuggestions.)")

    pickle.loads(pickle.dumps(mr))
    assert str(mr) == "MissingResource: FooBar"

    rnf = RevisionNotFound(DependentSet("revision"), 10)
    pickle.loads(pickle.dumps(rnf))
    assert str(
        rnf) == "RevisionNotFound: Could not find revision ({revision}:10)"

    pnf = PageNotFound(DependentSet("page"), 12)
    pickle.loads(pickle.dumps(pnf))
    assert str(pnf) == "PageNotFound: Could not find page ({page}:12)"

    unf = UserNotFound(DependentSet("user"), 10)
    pickle.loads(pickle.dumps(unf))
    assert str(unf) == "UserNotFound: Could not find user account ({user}:10)"

    ud = UserDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(ud))
    assert str(ud) == "UserDeleted: User deleted ({revision})"

    cd = CommentDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(cd))
    assert str(cd) == "CommentDeleted: Comment deleted ({revision})"

    td = TextDeleted(DependentSet("revision"))
    pickle.loads(pickle.dumps(td))
    assert str(td) == "TextDeleted: Text deleted ({revision})"

    cde = CaughtDependencyError("Test", RuntimeError("Foo"))
    pickle.loads(pickle.dumps(cde))
    assert str(cde) == "RuntimeError: Test\nNone"

    uct = UnexpectedContentType("Test", "JSON")
    pickle.loads(pickle.dumps(uct))
    assert str(uct) == ("UnexpectedContentType: "
                        "Expected content of type JSON, "
                        "but the following can't be parsed "
                        "(max 50 chars showed): Test")
