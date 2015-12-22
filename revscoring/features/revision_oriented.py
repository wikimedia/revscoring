import re

from ..datasources import revision_oriented
from .feature import Feature
from .meta import bools


class Revision:

    def __init__(self, prefix, revision_datasources):
        self.prefix = prefix
        self.datasources = revision_datasources

        if hasattr(revision_datasources, 'parent'):
            self.parent = Revision(
                prefix + ".parent",
                revision_datasources.parent
            )

        if hasattr(revision_datasources, 'page'):
            self.page = Page(
                prefix + ".page",
                revision_datasources.page
            )

        if hasattr(revision_datasources, 'user'):
            self.user = User(
                prefix + ".user",
                revision_datasources.user
            )

    def comment_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self.prefix + ".comment_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.comment,
                                 name=name)


class Page:
    def __init__(self, prefix, page_datasources):
        self.prefix = prefix
        self.datasources = page_datasources

        if hasattr(page_datasources, "namespace"):
            self.namespace = Namespace(prefix + ".namespace",
                                       page_datasources.namespace)

    def id_in_set(self, ids, name=None):
        if name is None:
            name = "{0}({1})".format(self.prefix + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def title_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self.prefix + ".title_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.title, name=name)


class Namespace:
    def __init__(self, prefix, namespace_datasources):
        self.prefix = prefix
        self.datasources = namespace_datasources

    def id_in_set(self, ids, name=None):
        if name is None:
            name = "{0}({1})".format(self.prefix + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id, name=name)

    def name_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self.prefix + ".name_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.name, name=name)


class User:

    def __init__(self, prefix, user_datasource):
        self.prefix = prefix
        self.datasources = user_datasource

    def id_in_set(self, ids, name=None):
        if name is None:
            name = "{0}({1})".format(self.prefix + ".id_in_set", repr(ids))

        return bools.set_contains_item(ids, self.datasources.id,
                                       name=name)

    def text_matches(self, regex, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})".format(self.prefix + ".text_matches",
                                     repr(regex.pattern))

        return bools.regex_match(regex, self.datasources.text, name=name)

    def in_group(self, groups, name=None):
        if name is None:
            name = "{0}({1})".format(self.prefix + ".in_group",
                                     repr(groups))

        return bools.sets_intersect(groups, self.datasources.groups, name=name)


revision = Revision("revision", revision_oriented.revision)
