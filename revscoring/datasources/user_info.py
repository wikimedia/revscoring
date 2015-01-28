from collections import namedtuple

from mw import Timestamp

from .datasource import Datasource
from .user_doc import user_doc

UserInfo = namedtuple("UserInfo", ['id', 'name', 'editcount', 'registration',
                                   'groups', 'implicitgroups', 'emailable',
                                   'gender', 'block_id', 'blocked_by',
                                   'blocked_by_id', 'block_reason',
                                   'block_expiry'])

def process(user_doc):
    
    try:
        registration = Timestamp(user_doc.get('registration'))
    except ValueError:
        registration = None
    
    return UserInfo(
        user_doc.get('userid'),
        user_doc.get('name'),
        user_doc.get('editcount'),
        registration,
        user_doc.get('groups', []),
        user_doc.get('implicitgroups', []),
        "emailable" in user_doc,
        user_doc.get('gender'),
        user_doc.get('block_id'),
        user_doc.get('blocked_by'),
        user_doc.get('blocked_by_id'),
        user_doc.get('block_reason'),
        user_doc.get('block_expiry')
    )

user_info = Datasource("user_info", process, depends_on=[user_doc])
