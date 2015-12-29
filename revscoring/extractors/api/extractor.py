import logging
from collections import defaultdict
from itertools import groupby, islice

import mwapi

from . import datasources
from .. import Extractor as BaseExtractor
from ...datasources import Datasource, revision_oriented
from ...dependencies import expand
from ...errors import RevisionNotFound, UserNotFound
from .revision_oriented import Revision
from .util import REV_PROPS, USER_PROPS

logger = logging.getLogger(__name__)


class Extractor(BaseExtractor):
    def __init__(self, session, context=None, cache=None):
        super().__init__(context=context, cache=cache)
        self.session = session
        self.dependents = Datasource("extractor.dependents")

        rev_doc = self.get_rev_doc_by_id(revision_oriented.revision)
        self.revision = Revision(
            revision_oriented.revision, self, rev_doc,
            id_datasource=revision_oriented.revision.id
        )

        # Registers revision_oriented context
        self.update(context=self.revision)

    def get_rev_doc_by_id(self, revision):
        return datasources.RevDocById(revision, self)

    def get_page_creation_rev_doc(self, page):
        return datasources.PageCreationRevDoc(page, self)

    def get_user_info_doc(self, user):
        return datasources.UserInfoDoc(user, self)

    def get_last_user_rev_doc(self, user):
        return datasources.LastUserRevDoc(user, self)

    def extract(self, rev_ids, dependents, context=None, cache=None):
        """
        Extracts a values for a set of
        :class:`~revscoring.dependents.dependent.Dependent` (e.g.
        :class:`~revscoring.features.feature.Feature` or
        :class:`~revscoring.datasources.datasource.Datasource`) for a revision
        or a set of revisions
        :Parameters:
            rev_ids : int | `iterable`
                Either a single rev_id or an `iterable` of rev_ids
            dependents : :class:`~revscoring.dependents.dependent.Dependent`
                A set of dependents to extract values for
            context : `dict` | `iterable`
                A set of call-specific
                :class:`~revscoring.dependents.dependent.Dependent` to inject
            cache : `dict`
                A set of call-specific pre-computed values to inject
        :Returns:
            An generator of extracted values if a single rev_id was provided or
            a genetator of (error, values) pairs where error is `None` if no
            error occured during extraction.
        """
        context = context or {}

        if hasattr(rev_ids, "__iter__"):
            return self._extract_many(rev_ids, dependents, context)
        else:
            rev_id = rev_ids
            return self._extract(rev_id, dependents, context, cache)

    def _extract_many(self, rev_ids, dependents, context):
        all_dependents = set(expand(dependents))

        revision_caches = defaultdict(lambda: {})

        errored = {}

        # Build up caches for data that can be queried in batch
        if self.revision & all_dependents:
            rvprop = set(REV_PROPS)
            if self.revision.text in all_dependents:
                rvprop.add('content')

            # Get revision data
            logger.info("Batch requesting {0} revision from the API"
                        .format(len(rev_ids)))
            rev_docs = self.get_rev_doc_map(rev_ids, rvprop=rvprop)
            for rev_id in rev_ids:
                if rev_id in rev_docs:
                    revision_caches[rev_id][self.revision.doc] = \
                        rev_docs[rev_id]
                else:
                    errored[rev_id] = RevisionNotFound(self.revision, rev_id)

            if self.revision.parent & all_dependents:
                parent_revs = {r.get('parentid'): r
                               for r in rev_docs.values()
                               if r.get('parentid', 0) > 0}

                logger.info("Batch requesting {0} revision.parent from the API"
                            .format(len(parent_revs)))
                parent_rev_docs = self.get_rev_doc_map(parent_revs.keys(),
                                                       rvprop=rvprop)

                for parent_id in parent_revs:
                    rev_doc = parent_revs[parent_id]
                    rev_id = rev_doc['revid']
                    if parent_id in parent_rev_docs:
                        revision_caches[rev_id][self.revision.parent.doc] = \
                            parent_rev_docs[parent_id]
                    else:
                        errored[rev_id] = \
                            RevisionNotFound(self.parent.revision, parent_id)

            if self.revision.user.info & all_dependents:
                user_revs = groupby((r for r in rev_docs.values()
                                     if r.get('userid', 0) > 0),
                                    lambda r: r.get('user'))
                user_texts = {ut: list(revs) for ut, revs in user_revs}
                logger.info("Batch requesting {0} revision.user.info from "
                            .format(len(user_texts)) + "the API")
                user_info_docs = self.get_user_doc_map(user_texts.keys(),
                                                       usprop=USER_PROPS)

                for user_text in user_texts:
                    rev_docs = user_texts[user_text]
                    for rev_doc in rev_docs:
                        rev_id = rev_doc['revid']
                        cache = revision_caches[rev_id]
                        if user_text in user_info_docs:
                            cache[self.revision.user.info.doc] = \
                                user_info_docs[user_text]
                        else:
                            errored[rev_id] = \
                                UserNotFound(self.revision.user, user_text)

        # Now extract dependent values one-by-one

        for rev_id in rev_ids:
            # If an error happened, give up hope
            if rev_id in errored:
                yield errored[rev_id], None
            else:
                # If no error happened, try to solve the other dependencies.
                try:
                    values = self._extract(rev_id, dependents, context=context,
                                           cache=revision_caches[rev_id])
                    yield None, list(values)
                except Exception as e:
                    yield e, None

    def _extract(self, rev_id, dependents, cache, context):
        all_dependents = set(expand(dependents))

        extract_cache = {self.revision.id: rev_id,
                         self.dependents: all_dependents}
        extract_cache.update(cache)
        return self.solve(dependents, context=context, cache=extract_cache)

    def get_rev_doc_map(self, rev_ids, rvprop={'ids', 'user', 'timestamp',
                                               'userid', 'comment', 'content',
                                               'flags', 'size'}):
        if len(rev_ids) == 0:
            return {}

        logger.debug("Building a map of {0} revisions: {1}"
                     .format(len(rev_ids), rev_ids))
        rev_docs = self.query_revisions_by_revids(rev_ids, rvprop=rvprop)

        return {rd['revid']: rd for rd in rev_docs}

    def query_revisions_by_revids(self, revids, batch=50, **params):
        revids_iter = iter(revids)
        while True:
            batch_ids = list(islice(revids_iter, 0, batch))
            if len(batch_ids) == 0:
                break
            else:
                doc = self.session.get(action='query', prop='revisions',
                                       revids=batch_ids, **params)

                for page_doc in doc['query'].get('pages', {}).values():
                    yield from _normalize_revisions(page_doc)

    def get_user_doc_map(self, user_texts,
                         usprop={'groups', 'registration', 'emailable',
                                 'editcount', 'gender'}):
        if len(user_texts) == 0:
            return {}
        logger.debug("Building a map of {0} user.info.docs"
                     .format(len(user_texts)))
        return {ud['name']: ud
                for ud in self.query_users_by_text(user_texts, usprop=usprop)}

    def query_users_by_text(self, user_texts, batch=50, **params):
        user_texts_iter = iter(user_texts)
        while True:
            batch_texts = list(islice(user_texts_iter, 0, batch))
            if len(batch_texts) == 0:
                break
            else:
                doc = self.session.get(action='query', list='users',
                                       ususers=batch_texts, **params)

                for user_doc in doc['query'].get('users', []):
                    yield user_doc

    def get_user_last_revision(self, user_text, rev_timestamp,
                               ucprop={'ids', 'timestamp', 'comment', 'size'}):
        if user_text is None or rev_timestamp is None:
            return None

        logger.debug("Requesting the last revision by {0} from the API"
                     .format(user_text))
        doc = self.session.get(action="query", list="usercontribs",
                               ucuser=user_text, ucprop=ucprop,
                               uclimit=1, ucdir="older",
                               ucstart=(rev_timestamp - 1))

        rev_docs = doc['query']['usercontribs']

        if len(rev_docs) > 0:
            return rev_docs[0]
        else:
            # It's OK to not find a revision here.
            return None

    def get_page_creation_doc(self, page_id,
                              rvprop={'ids', 'user', 'timestamp', 'userid',
                                      'comment', 'flags', 'size'}):
        if page_id is None:
            return None

        logger.debug("Requesting creation revision for ({0}) from the API"
                     .format(page_id))
        doc = self.session.get(action="query", prop="revisions",
                               pageids=page_id, rvdir="newer", rvlimit=1,
                               rvprop=rvprop)

        page_doc = doc['query'].get('pages', {'revisions': []}).values()
        rev_docs = page_doc['revisions']

        if len(rev_docs) == 1:
            return rev_docs[0]
        else:
            # This is bad, but it should be handled by the calling funcion
            return None

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        logger.info("Loading api.Extractor '{0}' from config.".format(name))
        section = config[section_key][name]
        kwargs = {k: v for k, v in section.items() if k != "class"}
        return cls(mwapi.Session(**kwargs))


def _normalize_revisions(page_doc):
    page_meta = {k: v for k, v in page_doc.items()
                 if k != 'revisions'}
    if 'revisions' in page_doc:
        for revision_doc in page_doc['revisions']:
            revision_doc['page'] = page_meta
            yield revision_doc
