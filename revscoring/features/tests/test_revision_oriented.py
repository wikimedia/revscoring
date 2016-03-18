from nose.tools import eq_

from ...dependencies import solve
from ..revision_oriented import revision


def test_comment_matches():
    starts_with_t = revision.comment_matches(r"^t")
    eq_(solve(starts_with_t, cache={revision.datasources.comment: "This"}),
        True)
    eq_(solve(starts_with_t, cache={revision.datasources.comment: "Foo"}),
        False)


def test_user_is_anon():
    eq_(solve(revision.user.is_anon, cache={revision.datasources.user.id: 0}),
        True)
    eq_(solve(revision.user.is_anon, cache={revision.datasources.user.id: 1}),
        False)


def test_user_text_matches():
    starts_with_t = revision.user.text_matches(r"^t")
    eq_(solve(starts_with_t, cache={revision.datasources.user.text: "This"}),
        True)
    eq_(solve(starts_with_t, cache={revision.datasources.user.text: "Foo"}),
        False)


def test_user_id_in_set():
    is_me = revision.user.id_in_set({6877667})
    eq_(solve(is_me, cache={revision.datasources.user.id: 6877667}),
        True)
    eq_(solve(is_me, cache={revision.datasources.user.id: 999}),
        False)


def test_user_in_group():
    is_bot_or_sysop = revision.user.in_group({'bot', 'sysop'})
    eq_(solve(is_bot_or_sysop,
              cache={revision.datasources.user.info.groups: {'bot'}}), True)
    eq_(solve(is_bot_or_sysop,
              cache={revision.datasources.user.info.groups: {'foo'}}), False)


def test_page_title_matches():
    starts_with_t = revision.page.title_matches(r"^t")
    eq_(solve(starts_with_t, cache={revision.datasources.page.title: "This"}),
        True)
    eq_(solve(starts_with_t, cache={revision.datasources.page.title: "Foo"}),
        False)


def test_page_id_in_set():
    is_binary = revision.page.id_in_set({0, 1})
    eq_(solve(is_binary, cache={revision.datasources.page.id: 0}),
        True)
    eq_(solve(is_binary, cache={revision.datasources.page.id: 999}),
        False)


def test_name_namespace_name_matches():
    starts_with_t = revision.page.namespace.name_matches(r"^t")
    eq_(solve(starts_with_t,
              cache={revision.datasources.page.namespace.name: "This"}),
        True)
    eq_(solve(starts_with_t,
              cache={revision.datasources.page.namespace.name: "Foo"}),
        False)


def test_page_namespace_id_in_set():
    wikipedia_namespace = revision.page.namespace.id_in_set({4, 5})
    eq_(solve(wikipedia_namespace,
              cache={revision.datasources.page.namespace.id: 5}),
        True)
    eq_(solve(wikipedia_namespace,
              cache={revision.datasources.page.namespace.id: 0}),
        False)
