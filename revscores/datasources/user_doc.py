from .datasource import Datasource
from .revision_metadata import revision_metadata


def process(session, revision_metadata):
    user_docs = session.users.query(
            users={revision_metadata.user_text},
            properties={'blockinfo', 'implicitgroups', 'groups', 'registration',
                        'emailable', 'editcount', 'gender'})
    
    user_docs = list(user_docs)
    if len(user_docs) >= 1:
        return user_docs[0]
    else:
        return None

user_doc = Datasource("user_doc", process,
                      depends_on=['session', revision_metadata])
