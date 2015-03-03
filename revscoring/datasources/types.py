class RevisionMetadata:
    __slots__ = ('rev_id', 'parent_id', 'user_text', 'user_id', 'timestamp',
                 'comment', 'page_id', 'page_namespace', 'page_title', 'bytes',
                 'minor')
    def __init__(self, rev_id, parent_id, user_text, user_id, timestamp,
                 comment, page_id, page_namespace, page_title, bytes, minor):
        self.rev_id = int(rev_id) if rev_id is not None else None
        self.parent_id = int(parent_id) if parent_id is not None else None
        self.user_text = str(user_text) if user_text is not None else None
        self.user_id = int(user_id) if user_id is not None else None
        self.timestamp = Timestamp(timestamp) if timestamp is not None else None
        self.comment = str(comment) if comment is not None else None
        self.page_id = int(page_id) if page_id is not None else None
        self.page_namespace = int(page_namespace) \
                              if page_namespace is not None else None
        self.page_title = str(page_title) if page_title is not None else None
        self.bytes = int(bytes) if bytes is not None else None
        self.minor = bool(minor)
    
    @classmethod
    def from_doc(cls, rev_doc):
        try:
            timestamp = Timestamp(rev_doc.get('timestamp'))
        except ValueError:
            timestamp = None
        
        return cls(rev_doc.get('revid'),
                   rev_doc.get('parentid'),
                   rev_doc.get('user'),
                   rev_doc.get('userid'),
                   timestamp,
                   rev_doc.get('comment'),
                   rev_doc.get('page', {}).get('pageid'),
                   rev_doc.get('page', {}).get('ns'),
                   rev_doc.get('page', {}).get('title'),
                   rev_doc.get('size'),
                   'minor' in rev_doc)

class UserInfo:
    __slots__ = ('id', 'name', 'editcount', 'registration',
                 'groups', 'implicitgroups', 'emailable',
                 'gender', 'block_id', 'blocked_by',
                 'blocked_by_id', 'blocked_timestamp', 'block_reason',
                 'block_expiry')
    
    def __init__(self, id, name, editcount, registration,
                 groups, implicitgroups, emailable,
                 gender, block_id, blocked_by,
                 blocked_by_id, blocked_timestamp, block_reason,
                 block_expiry)
        self.id = int(id) if id is not None else None
        self.name = str(name) if name is not None else None
        self.editcount = int(editcount) if editcount is not None else None
        self.registration = Timestamp(registration)
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
    
    def from_doc(cls, user_doc):
        try:
            registration = Timestamp(user_doc.get('registration'))
        except ValueError:
            registration = None
        
        cls(
            user_doc.get('userid'),
            user_doc.get('name'),
            user_doc.get('editcount'),
            registration,
            user_doc.get('groups', []),
            user_doc.get('implicitgroups', []),
            "emailable" in user_doc,
            user_doc.get('gender'),
            user_doc.get('blockid'),
            user_doc.get('blockedby'),
            user_doc.get('blockedbyid'),
            user_doc.get('blockedtimestamp'),
            user_doc.get('blockreason'),
            user_doc.get('blockexpiry')
        )
