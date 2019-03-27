
from revscoring.dependencies import solve
from revscoring.features.revision_oriented import revision


def test_comment_matches():
    starts_with_t = revision.comment_matches(r"^t")
    assert (solve(starts_with_t, cache={revision.datasources.comment: "This"}) is
            True)
    assert (solve(starts_with_t, cache={revision.datasources.comment: "Foo"}) is
            False)


def test_user_is_anon():
    assert (solve(revision.user.is_anon, cache={revision.datasources.user.id: 0}) is
            True)
    assert (solve(revision.user.is_anon, cache={revision.datasources.user.id: 1}) is
            False)


def test_user_text_matches():
    starts_with_t = revision.user.text_matches(r"^t")
    assert (solve(starts_with_t, cache={revision.datasources.user.text: "This"}) is
            True)
    assert (solve(starts_with_t, cache={revision.datasources.user.text: "Foo"}) is
            False)


def test_user_id_in_set():
    is_me = revision.user.id_in_set({6877667})
    assert (solve(is_me, cache={revision.datasources.user.id: 6877667}) is
            True)
    assert (solve(is_me, cache={revision.datasources.user.id: 999}) is
            False)


def test_user_in_group():
    is_bot_or_sysop = revision.user.in_group({'bot', 'sysop'})
    assert solve(is_bot_or_sysop,
                 cache={revision.datasources.user.info.groups: {'bot'}}) is True
    assert solve(is_bot_or_sysop,
                 cache={revision.datasources.user.info.groups: {'foo'}}) is False


def test_page_title_matches():
    starts_with_t = revision.page.title_matches(r"^t")
    assert (solve(starts_with_t, cache={revision.datasources.page.title: "This"}) is
            True)
    assert (solve(starts_with_t, cache={revision.datasources.page.title: "Foo"}) is
            False)


def test_page_id_in_set():
    is_binary = revision.page.id_in_set({0, 1})
    assert (solve(is_binary, cache={revision.datasources.page.id: 0}) is
            True)
    assert (solve(is_binary, cache={revision.datasources.page.id: 999}) is
            False)


def test_name_namespace_name_matches():
    starts_with_t = revision.page.namespace.name_matches(r"^t")
    assert (solve(starts_with_t,
                  cache={revision.datasources.page.namespace.name: "This"}) is
            True)
    assert (solve(starts_with_t,
                  cache={revision.datasources.page.namespace.name: "Foo"}) is
            False)


def test_page_namespace_id_in_set():
    wikipedia_namespace = revision.page.namespace.id_in_set({4, 5})
    assert (solve(wikipedia_namespace,
                  cache={revision.datasources.page.namespace.id: 5}) is
            True)
    assert (solve(wikipedia_namespace,
                  cache={revision.datasources.page.namespace.id: 0}) is
            False)
