import sys

from ..dependencies import DependentSet
from .datasource import Datasource

builtin_bytes = bytes


class Revision(DependentSet):

    def __init__(self, name,
                 include_parent=True,
                 include_user=True,
                 include_user_info=True,
                 include_user_last_revision=False,
                 include_page=True,
                 include_page_creation=False,
                 include_content=False):
        super().__init__(name)

        self.id = Datasource(name + ".id")
        self.timestamp = Datasource(name + ".timestamp")
        self.comment = Datasource(name + ".comment")
        self.byte_len = Datasource(name + ".byte_length")
        self.minor = Datasource(name + ".minor")
        self.content_model = Datasource(name + ".content_model")

        if include_content:
            self.text = Datasource(name + ".text")

        if include_parent:
            self.parent = Revision(
                name + ".parent",
                include_parent=False,
                include_user_info=False,
                include_page=False,
                include_content=include_content
            )

        if include_page:
            self.page = Page(
                name + ".page",
                include_creation=include_page_creation
            )

        if include_user:
            self.user = User(
                name + ".user",
                include_info=include_user_info,
                include_last_revision=include_user_last_revision
            )

        if include_content and include_parent:
            self.diff = Diff(
                name + ".diff"
            )


class User(DependentSet):

    def __init__(self, name, include_info=True,
                 include_last_revision=False):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        self.text = Datasource(name + ".text")

        if include_info:
            self.info = UserInfo(name + ".info")

        if include_last_revision:
            self.last_revision = Revision(
                name + ".last_revision",
                include_parent=False,
                include_user=False,
                include_content=False
            )


class UserInfo(DependentSet):
    def __init__(self, name):
        super().__init__(name)
        self.editcount = Datasource(name + ".editcount")
        self.registration = Datasource(name + ".registration")
        self.groups = Datasource(name + ".groups")
        self.emailable = Datasource(name + ".emailable")
        self.gender = Datasource(name + ".gender")


class Page(DependentSet):

    def __init__(self, name, include_creation=False):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        self.namespace = Namespace(name + ".namespace")
        self.title = Datasource(name + ".title")

        if include_creation:
            self.creation = Revision(
                name + ".creation",
                include_parent=False,
                include_page=False,
                include_content=False,
                include_user_last_revision=False
            )


class Namespace(DependentSet):

    def __init__(self, name):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        self.name = Datasource(name + ".name")


class Diff(DependentSet):

    def __init__(self, name):
        super().__init__(name)
        self.name = name


revision = Revision(
    "revision",
    include_page_creation=True,
    include_content=True,
    include_user_last_revision=True
)
