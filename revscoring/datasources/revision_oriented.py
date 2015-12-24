import sys

from .datasource import Datasource

builtin_bytes = bytes


class Revision:

    def __init__(self, prefix,
                 include_parent=True,
                 include_user=True,
                 include_user_info=True,
                 include_user_last_revision=False,
                 include_page=True,
                 include_page_creation=False,
                 include_content=False):
        self.prefix = prefix

        self.id = Datasource(prefix + ".id")
        self.parent_id = Datasource(prefix + ".parent_id")

        if include_parent:
            self.parent = Revision(
                prefix + ".parent",
                include_parent=False,
                include_user_info=False,
                include_page=False,
                include_content=include_content
            )

        if include_page:
            self.page = Page(
                prefix + ".page",
                include_creation=include_page_creation
            )

        if include_user:
            self.user = User(
                prefix + ".user",
                include_info=include_user_info,
                include_last_revision=include_user_last_revision
            )

        self.timestamp = Datasource(prefix + ".timestamp")
        self.comment = Datasource(prefix + ".comment")
        self.byte_len = Datasource(prefix + ".byte_length")
        self.minor = Datasource(prefix + ".minor")
        self.content_model = \
            Datasource(prefix + ".content_model")
        self.content_format = \
            Datasource(prefix + ".content_format")

        if include_content:
            self.text = Datasource(prefix + ".text")
            self.bytes = Datasource(
                prefix + ".bytes", _process_bytes,
                depends_on=[self.text]
            )

        if include_content and include_parent:
            self.diff = Diff(
                prefix + ".diff"
            )


class User:

    def __init__(self, prefix, include_info=True,
                 include_last_revision=False):
        self.prefix = prefix
        self.id = Datasource(prefix + ".id")
        self.text = Datasource(prefix + ".text")
        if include_info:
            self.editcount = Datasource(prefix + ".editcount")
            self.registration = Datasource(prefix + ".registration")
            self.groups = Datasource(prefix + ".groups")
            self.emailable = Datasource(prefix + ".emailable")
            self.gender = Datasource(prefix + ".gender")
            self.block_id = Datasource(prefix + ".block_id")
            self.blocked_by = Datasource(prefix + ".blocked_by")
            self.blocked_by_id = Datasource(prefix + ".blocked_by_id")
            self.blocked_timestamp = Datasource(prefix + ".blocked_timestamp")
            self.block_reason = Datasource(prefix + ".block_reason")
            self.block_expiry = Datasource(prefix + ".block_expiry")

        if include_last_revision:
            self.last_revision = Revision(
                prefix + ".last_revision",
                include_parent=False,
                include_user=False,
                include_content=False
            )


class Page:

    def __init__(self, prefix, include_creation=False):
        self.prefix = prefix
        self.id = Datasource(prefix + ".id")
        self.namespace = Namespace(prefix + ".namespace")
        self.title = Datasource(prefix + ".title")

        if include_creation:
            self.creation = Revision(
                prefix + ".creation",
                include_parent=False,
                include_page=False,
                include_content=False,
                include_user_last_revision=False
            )


class Namespace:

    def __init__(self, prefix):
        self.prefix = prefix
        self.id = Datasource(prefix + ".id")
        self.name = Datasource(prefix + ".name")


class Diff:

    def __init__(self, prefix):
        self.prefix = prefix


def _process_bytes(text):
    # TODO: Figure out a way to not assume UTF-8
    return builtin_bytes(text, "utf8", "replace")


revision = Revision(
    "revision",
    include_page_creation=True,
    include_content=True,
    include_user_last_revision=True
)
