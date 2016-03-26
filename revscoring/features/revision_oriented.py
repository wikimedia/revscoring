"""
A revision-oriented nesting of basic features.

.. autodata:: revscoring.features.revision_oriented.revision

.. autoclass:: revscoring.features.revision_oriented.Revision
    :members:

.. autoclass:: revscoring.features.revision_oriented.Page
    :members:

.. autoclass:: revscoring.features.revision_oriented.Namespace
    :members:

.. autoclass:: revscoring.features.revision_oriented.User
    :members:

"""

import re

from ..datasources import revision_oriented
from ..dependencies import DependentSet
from .feature import Feature
from .meta import bools


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        if hasattr(revision_datasources, 'parent'):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )
            """
            :class:`~revscoring.features.revision_oriented.Revision` features
            for the parent revision.
            """

        if hasattr(revision_datasources, 'page'):
            self.page = Page(
                name + ".page",
                revision_datasources.page
            )
            """
            :class:`~revscoring.features.revision_oriented.Page` features
            for the revision's page
            """

        if hasattr(revision_datasources, 'user'):
            self.user = User(
                name + ".user",
                revision_datasources.user
            )
            """
            :class:`~revscoring.features.revision_oriented.User` features
            for the revision's user
            """

    def comment_matches(self, regex, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True when the
        revision's comment matches `regex`.

        :Parameters:
            regex : `str` | `re.compile`
                The regex to match.  Case-insensitive by default.
            name : `str`
                A name for the new feature.
        """
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".comment_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.comment,
                                 name=name)


class Page(DependentSet):
    def __init__(self, name, page_datasources):
        super().__init__(name)
        self.datasources = page_datasources

        if hasattr(page_datasources, "namespace"):
            self.namespace = Namespace(name + ".namespace",
                                       page_datasources.namespace)
            """
            :class:`~revscoring.features.revision_oriented.Namespace` features
            for the revision's page's namespace.
            """

    def id_in_set(self, ids, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the page's
        ID appears within the provided set of IDs.

        :Parameters:
            ids : `set` ( `int` )
                A set of IDs to match against the page's ID
            name : `str`
                A name for the new feature.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def title_matches(self, regex, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the page's
        title (namespace excluded) matches `regex`.

        :Parameters:
            regex : `str` | `re.compile`
                The regex to match.  Case-insensitive by default.
            name : `str`
                A name for the new feature.
        """
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".title_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.title, name=name)


class Namespace(DependentSet):
    def __init__(self, name, namespace_datasources):
        super().__init__(name)
        self.datasources = namespace_datasources

    def id_in_set(self, ids, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the
        namespaces's ID appears within the provided set of IDs.

        :Parameters:
            ids : `set` ( `int` )
                A set of IDs to match against the namespaces's ID
            name : `str`
                A name for the new feature.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def name_matches(self, regex, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the
        namespace's name matches `regex`.

        :Parameters:
            regex : `str` | `re.compile`
                The regex to match.  Case-insensitive by default.
            name : `str`
                A name for the new feature.
        """
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".name_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.name, name=name)


class User(DependentSet):

    def __init__(self, name, user_datasources):
        super().__init__(name)
        self.datasources = user_datasources

        self.is_anon = Feature(self._name + ".is_anon", _process_is_anon,
                               returns=bool, depends_on=[self.datasources.id])

    def id_in_set(self, ids, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the
        user's ID appears within the provided set of IDs.

        :Parameters:
            ids : `set` ( `int` )
                A set of IDs to match against the user's ID
            name : `str`
                A name for the new feature.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id,
                                       name=name)

    def text_matches(self, regex, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the
        user's text (IP or username) matches `regex`.

        :Parameters:
            regex : `str` | `re.compile`
                The regex to match.  Case-insensitive by default.
            name : `str`
                A name for the new feature.
        """
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".text_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.text, name=name)

    def in_group(self, groups, name=None):
        """
        Generates a :class:`revscoring.Feature` that returns True the
        user is in a set of `groups`

        :Parameters:
            groups : `set` ( `str` )
                A set of group name's to search within.
            name : `str`
                A name for the new feature.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".in_group",
                                     repr(groups))

        return bools.sets_intersect(groups, self.datasources.info.groups,
                                    name=name)


def _process_is_anon(user_id):
    return user_id == 0

revision = Revision("revision", revision_oriented.revision)
"""
:class:`~revscoring.features.revision_oriented.Revision` features.
The base of revision-orientation.
"""
