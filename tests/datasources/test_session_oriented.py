from revscoring.datasources.session_oriented import rewrite_name, session

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
