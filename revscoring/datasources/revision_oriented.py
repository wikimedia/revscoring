import sys

from ..dependencies import DependentSet
from .datasource import Datasource

builtin_bytes = bytes


class Revision(DependentSet):

    def __init__(self, prefix,
                 include_parent=True,
                 include_user=True,
                 include_user_info=True,
                 include_user_last_revision=False,
                 include_page=True,
                 include_page_creation=False,
                 include_content=False):
        super().__init__(prefix)

        self.id = Datasource(prefix + ".id")
        self.timestamp = Datasource(prefix + ".timestamp")
        self.comment = Datasource(prefix + ".comment")
        self.byte_len = Datasource(prefix + ".byte_length")
        self.minor = Datasource(prefix + ".minor")
        self.content_model = Datasource(prefix + ".content_model")

        if include_content:
            self.text = Datasource(prefix + ".text")

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

        if include_content and include_parent:
            self.diff = Diff(
                prefix + ".diff"
            )


class User(DependentSet):

    def __init__(self, prefix, include_info=True,
                 include_last_revision=False):
        super().__init__(prefix)
        self.id = Datasource(prefix + ".id")
        self.text = Datasource(prefix + ".text")

        if include_info:
            self.info = UserInfo(prefix + ".info")

        if include_last_revision:
            self.last_revision = Revision(
                prefix + ".last_revision",
                include_parent=False,
                include_user=False,
                include_content=False
            )


class UserInfo(DependentSet):
    def __init__(self, prefix):
        super().__init__(prefix)
        self.editcount = Datasource(prefix + ".editcount")
        self.registration = Datasource(prefix + ".registration")
        self.groups = Datasource(prefix + ".groups")
        self.emailable = Datasource(prefix + ".emailable")
        self.gender = Datasource(prefix + ".gender")


class Page(DependentSet):

    def __init__(self, prefix, include_creation=False):
        super().__init__(prefix)
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


class Namespace(DependentSet):

    def __init__(self, prefix):
        super().__init__(prefix)
        self.id = Datasource(prefix + ".id")
        self.name = Datasource(prefix + ".name")


class Diff(DependentSet):

    def __init__(self, prefix):
        super().__init__(prefix)
        self.prefix = prefix


revision = Revision(
    "revision",
    include_page_creation=True,
    include_content=True,
    include_user_last_revision=True
)
