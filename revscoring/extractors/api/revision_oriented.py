import logging

import mwtypes

from ...datasources import Datasource
from ...dependencies import DependentSet
from ...errors import CommentDeleted, TextDeleted, UserDeleted
from .util import key, key_exists, or_none

logger = logging.getLogger(__name__)


class Revision(DependentSet):
    def __init__(self, revision, extractor, rev_doc, id_datasource=None):
        super().__init__(revision._name)

        self.doc = rev_doc

        self.id = id_datasource or key('revid', rev_doc, name=revision.id.name)

        self.timestamp = key('timestamp', rev_doc,
                             name=revision.timestamp.name,
                             apply=mwtypes.Timestamp)
        self.comment = key('comment', rev_doc, name=revision.comment.name,
                           if_missing=(CommentDeleted, revision.comment))
        self.byte_len = key('byte_len', rev_doc,
                            name=revision.byte_len.name)
        self.minor = key_exists('minor', rev_doc,
                                name=revision.minor.name)
        self.content_model = key('contentmodel', rev_doc,
                                 revision.content_model.name)

        if hasattr(revision, 'text'):
            self.text = key('*', rev_doc, name=revision.text.name,
                            if_missing=(TextDeleted, revision.text))

        if hasattr(revision, 'parent'):
            parent_id = key('parentid', rev_doc, name=revision.parent.id.name)
            parent_doc = extractor.get_rev_doc_by_id(revision.parent)
            self.parent = Revision(revision.parent, extractor, parent_doc,
                                   id_datasource=parent_id)

        if hasattr(revision, 'page'):
            self.page = RevisionPage(revision.page, extractor, rev_doc)

        if hasattr(revision, 'user'):
            self.user = RevisionUser(revision, extractor, rev_doc)


class RevisionPage(DependentSet):

    def __init__(self, page, extractor, rev_doc):
        super().__init__(page._name)
        namespace_title = Datasource(
            page._name + ".namespace_title", normalize_title,
            depends_on=[rev_doc]
        )
        self.id = key(['page', 'pageid'], rev_doc, name=page.id.name)
        self.title = Datasource(page.title.name, second,
                                depends_on=[namespace_title])
        self.namespace = Namespace(page.namespace, extractor, rev_doc,
                                   namespace_title)

        if hasattr(page, 'creation'):
            page_creation_doc = extractor.get_page_creation_rev_doc(page)
            self.creation = Revision(page.creation, extractor,
                                     page_creation_doc)


class Namespace(DependentSet):
    def __init__(self, namespace, extractor, rev_doc, namespace_title):
        super().__init__(namespace._name)
        self.id = key(['page', 'ns'], rev_doc, name=namespace.id.name)
        self.name = Datasource(namespace.name.name, first,
                               depends_on=[namespace_title])


class RevisionUser(DependentSet):

    def __init__(self, revision, extractor, rev_doc):
        super().__init__(revision.user._name)
        self.id = key('userid', rev_doc, name=revision.user.id.name,
                      if_missing=(UserDeleted, revision.user))
        self.text = key('user', rev_doc, name=revision.user.text.name,
                        if_missing=(UserDeleted, revision.user))

        if hasattr(revision.user, 'info'):
            self.info = RevisionUserInfo(revision.user, extractor)

        if hasattr(revision.user, 'last_revision'):
            lur_doc = extractor.get_last_user_rev_doc(revision)
            self.last_revision = Revision(revision.user.last_revision,
                                          extractor, lur_doc)


class RevisionUserInfo(DependentSet):

    def __init__(self, user, extractor):
        super().__init__(user.info._name)

        self.doc = extractor.get_user_info_doc(user)
        self.editcount = key('editcount', self.doc,
                             name=user.info.editcount.name)
        self.registration = key('registration', self.doc,
                                name=user.info.registration.name,
                                apply=or_none(mwtypes.Timestamp))
        self.groups = key('groups', self.doc, name=user.info.groups.name,
                          apply=set)
        self.emailable = key_exists('emailable', self.doc,
                                    name=user.info.emailable.name)
        self.gender = key('gender', self.doc, name=user.info.gender.name)


def normalize_title(rev_doc):
    if 'page' in rev_doc and 'title' in rev_doc['page']:
        page_name = rev_doc['page']['title']
        if rev_doc['page']['ns'] > 0:
            parts = page_name.split(":", 1)
            if len(parts) == 2:
                return parts[0], parts[1]
            else:
                return "", page_name
        else:
            return "", page_name
    else:
        return None, None


def first(pair):
    return pair[0]


def second(pair):
    return pair[1]
