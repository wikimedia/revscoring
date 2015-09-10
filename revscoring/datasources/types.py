"""
.. autoclass:: RevisionMetadata

.. autoclass:: UserInfo
"""
from mwtypes import Timestamp


class RevisionMetadata:
    """
    Represents a revision's metadata.
    """
    __slots__ = ('rev_id', 'parent_id', 'user_text', 'user_id', 'timestamp',
                 'comment', 'page_id', 'page_namespace', 'page_title', 'bytes',
                 'minor')

    def __init__(self, rev_id=None, parent_id=None, user_text=None,
                 user_id=None, timestamp=None, comment=None, page_id=None,
                 page_namespace=None, page_title=None, bytes=None, minor=None):
        self.rev_id = int(rev_id) if rev_id is not None else None
        self.parent_id = int(parent_id) if parent_id is not None else None
        self.user_text = str(user_text) if user_text is not None else None
        self.user_id = int(user_id) if user_id is not None else None
        self.timestamp = Timestamp(timestamp) \
            if timestamp is not None else None
        self.comment = str(comment) if comment is not None else None
        self.page_id = int(page_id) if page_id is not None else None
        self.page_namespace = int(page_namespace) \
            if page_namespace is not None else None
        self.page_title = str(page_title) if page_title is not None else None
        self.bytes = int(bytes) if bytes is not None else None
        self.minor = bool(minor)


class UserInfo:
    """
    Represents information about a user.
    """
    __slots__ = ('id', 'name', 'editcount', 'registration',
                 'groups', 'implicitgroups', 'emailable',
                 'gender', 'block_id', 'blocked_by',
                 'blocked_by_id', 'blocked_timestamp', 'block_reason',
                 'block_expiry')

    def __init__(self, id=None, name=None, editcount=None, registration=None,
                 groups=None, implicitgroups=None, emailable=None,
                 gender=None, block_id=None, blocked_by=None,
                 blocked_by_id=None, blocked_timestamp=None, block_reason=None,
                 block_expiry=None):
        self.id = int(id) if id is not None else None
        self.name = str(name) if name is not None else None
        self.editcount = int(editcount) if editcount is not None else None
        self.registration = Timestamp(registration) \
            if registration is not None else None
        self.groups = groups or []
        self.implicitgroups = implicitgroups or []
        self.emailable = bool(emailable)
        self.gender = str(gender) if gender is not None else None
        self.block_id = int(block_id) if block_id is not None else None
        self.blocked_by = str(blocked_by) if blocked_by is not None else None
        self.blocked_by_id = int(blocked_by_id) \
            if blocked_by_id is not None else None
        self.blocked_timestamp = Timestamp(blocked_timestamp) \
            if blocked_timestamp is not None else None
        self.block_reason = str(block_reason) \
            if block_reason is not None else None
        self.block_expiry = str(block_expiry) \
            if block_expiry is not None else None
