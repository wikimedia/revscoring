"""
Implements a set of datasources oriented off of a single revision.  This is
useful for extracting features of edit and article quality.

.. autodata:: revscoring.datasources.revision_oriented.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.datasources.revision_oriented.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.Diff
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.Page
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.Namespace
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.User
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.UserInfo
    :members:
    :member-order: bysource

"""
from ..dependencies import DependentSet
from .datasource import Datasource


class Revision(DependentSet):
    """
    Represents a revision
    """

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
        "`int` : Revision ID"
        self.timestamp = Datasource(name + ".timestamp")
        ":class:`mwtypes.Timestamp` : Timestamp the revision was saved"
        self.comment = Datasource(name + ".comment")
        "`str` : The comment saved with the revision"
        self.byte_len = Datasource(name + ".byte_length")
        "`int` : The length of the revision content in bytes"
        self.minor = Datasource(name + ".minor")
        "`bool` : Was the revision flagged as minor?"
        self.content_model = Datasource(name + ".content_model")
        "`str` : Describes the format of revision content"

        if include_content:
            self.text = Datasource(name + ".text")
            "`str` : The decoded (Unicode) text of the revision content"

        if include_parent:
            self.parent = Revision(
                name + ".parent",
                include_parent=False,
                include_user_info=False,
                include_page=False,
                include_content=include_content
            )
            """
            :class:`~revscoring.datasources.revision_oriented.Revision` : The
            parent (aka "previous") revision of the page.
            """

        if include_page:
            self.page = Page(
                name + ".page",
                include_creation=include_page_creation
            )
            """
            :class:`~revscoring.datasources.revision_oriented.Page` : The
            page in which the revision was saved.
            """

        if include_user:
            self.user = User(
                name + ".user",
                include_info=include_user_info,
                include_last_revision=include_user_last_revision
            )
            """
            :class:`~revscoring.datasources.revision_oriented.User` : The
            user who saved the revision.
            """

        if include_content and include_parent:
            self.diff = Diff(
                name + ".diff"
            )
            """
            :class:`~revscoring.datasources.revision_oriented.Diff` : The
            difference between this revision and the parent revision.
            """


class User(DependentSet):
    """
    Represents a user's id and name/ip
    """

    def __init__(self, name, include_info=True,
                 include_last_revision=False):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        "`int` : The id of the user who saved the edit.  0 for IPs."
        self.text = Datasource(name + ".text")
        "`str` : The user's name or IP address"

        if include_info:
            self.info = UserInfo(name + ".info")
            """
            :class:`~revscoring.datasources.revision_oriented.UserInfo` :
            Information about the user.
            """

        if include_last_revision:
            self.last_revision = Revision(
                name + ".last_revision",
                include_parent=False,
                include_user=False,
                include_content=False
            )
            """
            :class:`~revscoring.datasources.revision_oriented.Revision` : The
            last revision the user saved before the revision of reference.
            """


class UserInfo(DependentSet):
    """
    Represents a user's information
    """

    def __init__(self, name):
        super().__init__(name)
        self.editcount = Datasource(name + ".editcount")
        "`int` : A count of edits the user has ever saved"
        self.registration = Datasource(name + ".registration")
        ":class:`mwtypes.Timestamp` : The date the user registered"
        self.groups = Datasource(name + ".groups")
        "`set` ( `str` ) : The groups the user is a member of"
        self.emailable = Datasource(name + ".emailable")
        "`bool` : `True` if the users is emailable, `False` otherwise"
        self.gender = Datasource(name + ".gender")
        "`str` : A string representing the user's ``gender`` preference."


class Page(DependentSet):
    """
    Represents a revision's page
    """

    def __init__(self, name, include_creation=False):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        "`int` : The page's ID"
        self.title = Datasource(name + ".title")
        "`str` : The page's title (namespace stripped)"
        self.namespace = Namespace(name + ".namespace")
        """
        :class:`~revscoring.datasources.revision_oriented.Namespace` : The
        namespace information.
        """

        if include_creation:
            self.creation = Revision(
                name + ".creation",
                include_parent=False,
                include_page=False,
                include_content=False,
                include_user_last_revision=False
            )
            """
            :class:`~revscoring.datasources.revision_oriented.Revision` : The
            first revision to the page.
            """


class Namespace(DependentSet):
    """
    Represents a page's namespace
    """

    def __init__(self, name):
        super().__init__(name)
        self.id = Datasource(name + ".id")
        "`int` : The namespace's ID"
        self.name = Datasource(name + ".name")
        "`str` : The name of the namespace"


class Diff(DependentSet):
    """
    Represents the difference between two sequential revisions.
    """

    def __init__(self, name):
        super().__init__(name)

revision = Revision(
    "revision",
    include_page_creation=True,
    include_content=True,
    include_user_last_revision=True
)
"""
Represents the base revision of interest.  Implements this structure:

* revision: :class:`~revscoring.datasources.revision_oriented.Revision`
    * diff: :class:`~revscoring.datasources.revision_oriented.Diff`
    * user: :class:`~revscoring.datasources.revision_oriented.User`
        * info: :class:`~revscoring.datasources.revision_oriented.UserInfo`
        * last_revision:
            * page: :class:`~revscoring.datasources.revision_oriented.Page`
                * namespace: :class:`~revscoring.datasources.revision_oriented.Namespace`
    * page: :class:`~revscoring.datasources.revision_oriented.Page`
        * namespace: :class:`~revscoring.datasources.revision_oriented.Namespace`
        * creation: :class:`~revscoring.datasources.revision_oriented.Revision`
    * parent: :class:`~revscoring.datasources.revision_oriented.Revision`
        * user: :class:`~revscoring.datasources.revision_oriented.User`
"""  # noqa
