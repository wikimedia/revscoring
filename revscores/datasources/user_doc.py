from ..util.dependencies import depends
from .revision_metadata import revision_metadata


@depends(on=['session', revision_metadata])
def user_doc(session, revision_metadata):
    user_docs = session.users.query(
            users={revision_metadata.user_text},
            properties={'blockinfo', 'implicitgroups', 'groups', 'registration',
                        'emailable', 'editcount', 'gender'})
    
    if len(user_docs) >= 1:
        return user_docs[0]
    else:
        return None
