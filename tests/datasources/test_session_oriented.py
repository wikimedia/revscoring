from mwtypes import Timestamp
from revscoring import Datasource
from revscoring.datasources.session_oriented import (list_of_tree,
                                                     rewrite_name, session)
from revscoring.dependencies import DependentSet, solve

from .util import check_datasource


def test_session():
    check_datasource(session.revisions.id)
    check_datasource(session.revisions.timestamp)
    check_datasource(session.revisions.comment)
    check_datasource(session.revisions.byte_len)
    check_datasource(session.revisions.minor)
    check_datasource(session.revisions.content_model)
    check_datasource(session.revisions.text)
    assert hasattr(session.revisions, "parent")
    assert hasattr(session.revisions, "page")
    assert hasattr(session.revisions, "diff")

    # revision.parent
    check_datasource(session.revisions.parent.id)
    assert hasattr(session.revisions.parent, "user")
    check_datasource(session.revisions.parent.user.id)
    check_datasource(session.revisions.parent.user.text)
    assert not hasattr(session.revisions.parent.user, "info")
    check_datasource(session.revisions.parent.timestamp)
    check_datasource(session.revisions.parent.comment)
    check_datasource(session.revisions.parent.byte_len)
    check_datasource(session.revisions.parent.minor)
    check_datasource(session.revisions.parent.content_model)
    check_datasource(session.revisions.parent.text)
    assert not hasattr(session.revisions.parent, "page")
    assert not hasattr(session.revisions.parent, "parent")
    assert not hasattr(session.revisions.parent, "diff")

    # revision.page
    check_datasource(session.revisions.page.id)
    assert hasattr(session.revisions.page, "namespace")
    check_datasource(session.revisions.page.namespace.id)
    check_datasource(session.revisions.page.namespace.name)
    check_datasource(session.revisions.page.title)
    assert hasattr(session.revisions.page, "creation")
    check_datasource(session.revisions.page.creation.id)
    assert hasattr(session.revisions.page.creation, "user")
    check_datasource(session.revisions.page.creation.timestamp)
    check_datasource(session.revisions.page.creation.comment)
    check_datasource(session.revisions.page.creation.byte_len)
    check_datasource(session.revisions.page.creation.minor)
    check_datasource(session.revisions.page.creation.content_model)
    assert not hasattr(session.revisions.page.creation, "page")
    assert not hasattr(session.revisions.page.creation, "text")
    assert not hasattr(session.revisions.page.creation, "diff")
    assert hasattr(session.revisions.page, "suggested")
    check_datasource(session.revisions.page.suggested.properties)

    # revision.page.creation.user
    check_datasource(session.revisions.page.creation.user.id)
    check_datasource(session.revisions.page.creation.user.text)
    assert hasattr(session.revisions.page.creation.user, "info")
    check_datasource(session.revisions.page.creation.user.info.editcount)
    check_datasource(session.revisions.page.creation.user.info.registration)
    check_datasource(session.revisions.page.creation.user.info.groups)
    check_datasource(session.revisions.page.creation.user.info.emailable)
    check_datasource(session.revisions.page.creation.user.info.gender)

    # revision.user
    check_datasource(session.user.id)
    check_datasource(session.user.text)
    assert hasattr(session.user, "info")
    check_datasource(session.user.info.editcount)
    check_datasource(session.user.info.registration)
    check_datasource(session.user.info.groups)
    check_datasource(session.user.info.emailable)
    check_datasource(session.user.info.gender)


def test_rewrite_name():
    assert rewrite_name("revision.text") == "session.revisions.text"
    assert rewrite_name("bytes.revision.foobar") == \
           "bytes.session.revisions.foobar"
    assert rewrite_name("session.revisions.text") == "session.revisions.text"


def test_timestamp_str():
    cache = {session.revisions.timestamp_str: ["1970-01-01T00:00:00Z"]}
    assert solve(session.revisions.timestamp, cache=cache) == [Timestamp(0)]


def test_list_of_meta():
    text = Datasource("text")

    class contains(Datasource):

        def __init__(self, string_datasource, value, name=None):
            name = self._format_name(name, [string_datasource, value])
            super().__init__(name, self.process, depends_on=[string_datasource])
            self.value = value

        def process(self, string):
            return self.value in string

    def text_contains(value):
        return contains(text, value)


def test_list_of_tree():
    class TestThing(DependentSet):

        def __init__(self, name):
            super().__init__(name)
            self.text = Datasource(name + ".text")
            self.len = Datasource(
                name + ".text.len", self._process_len, depends_on=[self.text])

        @staticmethod
        def _process_len(text):
            return len(text)

        @DependentSet.meta_dependent
        def contains(self, value):
            return contains(
                self.text, value,
                name=self.name + ".text.contains({0!r})".format(value))

    class contains(Datasource):

        def __init__(self, string_datasource, value, name=None):
            name = self._format_name(name, [string_datasource, value])
            super().__init__(name, self.process, depends_on=[string_datasource])
            self.value = value

        def process(self, string):
            return self.value in string

    thing = TestThing("thing")
    cache = {thing.text: "Hello"}
    assert solve(thing.len, cache=cache) == 5
    assert solve(thing.contains("el"), cache=cache)
    assert not solve(thing.contains("Foobar"), cache=cache)

    list_of_thing = list_of_tree(
        TestThing("thing"),
        rewrite_name=lambda n: "list_of_" + n if not n.startswith("list_of_") else n)

    cache = {list_of_thing.text: ["Hello", "Foobar"]}
    assert solve(list_of_thing.len, cache=cache) == [5, 6]
    assert solve(list_of_thing.contains("el"), cache=cache) == [True, False]
    assert solve(list_of_thing.contains("Foobar"), cache=cache) == [False, True]
