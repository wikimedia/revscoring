from .datasource import Datasource

info = Datasource("user.info")
"""
Returns a :class:`~revscoring.datasources.types.UserInfo` for the user who
saved the current revision
"""


def process_user_groups(user_info):
    return set(user_info.groups + user_info.implicitgroups)

groups = Datasource("user.groups", process_user_groups, depends_on=[info])
"""
Returns a set of user_groups that the user belongs to -- both implicitly and
explicitly
"""
