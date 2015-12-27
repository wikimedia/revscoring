import re

from ..datasources import revision_oriented
from ..dependencies import DependentSet
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

        if hasattr(revision_datasources, 'page'):
            self.page = Page(
                name + ".page",
                revision_datasources.page
            )

        if hasattr(revision_datasources, 'user'):
            self.user = User(
                name + ".user",
                revision_datasources.user
            )

    def comment_matches(self, regex, name=None):
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

    def id_in_set(self, ids, name=None):
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def title_matches(self, regex, name=None):
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
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def name_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".name_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.name, name=name)


class User(DependentSet):

    def __init__(self, name, user_datasource):
        super().__init__(name)
        self.datasources = user_datasource

    def id_in_set(self, ids, name=None):
        if name is None:
            name = "{0}({1})".format(self._name + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id,
                                       name=name)

    def text_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self._name + ".text_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.text, name=name)

    def in_group(self, groups, name=None):
        if name is None:
            name = "{0}({1})".format(self._name + ".in_group",
                                     repr(groups))

        return bools.sets_intersect(groups, self.datasources.info.groups,
                                    name=name)


revision = Revision("revision", revision_oriented.revision)
