from . import revision
from .datasource import Datasource
from .types import UserInfo


def process_doc(session, revision_metadata):
    user_docs = session.users.query(
        users={revision_metadata.user_text},
        properties={'blockinfo', 'implicitgroups', 'groups', 'registration',
                    'emailable', 'editcount', 'gender'})

    user_docs = list(user_docs)
    if len(user_docs) >= 1:
        return user_docs[0]
    else:
        return None

doc = Datasource("user.doc", process_doc,
                 depends_on=['session', revision.metadata])


def process_info(user_doc):
    if user_doc is None:
        return None
    else:
        return UserInfo.from_doc(user_doc)

info = Datasource("user.info", process_info, depends_on=[doc])
