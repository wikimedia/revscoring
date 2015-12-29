from nose.tools import eq_

from .. import types, user
from ...dependencies import solve


def test_user_groups():
    user_info = types.UserInfo(groups=["foo", "bar"], implicitgroups=["derp"])

    eq_(solve(user.groups, cache={user.info: user_info}),
        {'foo', 'bar', 'derp'})
