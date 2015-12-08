from ...datasources import revision
from ...dependencies import solve


def test_comment_matches():
    has_foo = revision.comment_matches('.*foo.*')

    {revision.metadata: {comment: "Bar waffle hats banana"}}
    eq_(solve(has_foo, cache=),
        False)

    eq_(solve(has_foo, cache={comment: "Here comes the foobar!"}),
        True)

    eq_(has_foo,
        pickle.loads(pickle.dumps(has_foo)))
