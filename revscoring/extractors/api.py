import logging
from collections import defaultdict

from mw import Namespace, Timestamp, api

import yamlconf

from .. import dependencies
from ..datasources import (Datasource, RevisionMetadata, UserInfo,
                           parent_revision, revision, site, user)
from ..errors import RevisionDocumentNotFound
from ..languages import Language
from .extractor import Extractor

logger = logging.getLogger('revscoring.extractors.api')

revision_doc = Datasource("revision.doc")
parent_revision_doc = Datasource("parent_revision.doc")
previous_user_revision_doc = Datasource("previous_user_revision.doc")
page_creation_doc = Datasource("page_creation.doc")
user_doc = Datasource("user.doc")
site_doc = Datasource("site.doc")

class APIExtractor(Extractor):
    """
    Implements a :class:`~revscoring.extractor.extractor.Extractor` using a
    MediaWiki API.

    :Parameters:
        session : :class:`mw.api.Session`
            An API session to use
        language : :class:`~revscoring.languages.language.Language`
            A language context to use when extracting
        context : `dict` | `iterable`
            A collection of `~revscoring.dependencies.dependent.Dependent` to
            inject when extracting.
        cache : `dict`
            A collection of pre-computed values to inject when extracting
    """
    def __init__(self, session, language=None, context=None, cache=None):
        cache = cache or {}
        context = dependencies.normalize_context(context)

        self.session = session
        self.language = language

        local_cache = {
            site.namespace_map: self.get_namespace_map()
        }
        local_context = {d:d for d in [
            Datasource("revision.doc", self.process_revision_doc,
                       depends_on=[revision.id]),
            Datasource("revision.metadata", self.process_revision_metadata,
                       depends_on=[revision_doc]),
            Datasource("revision.text", self.process_revision_text,
                       depends_on=[revision_doc]),
            Datasource("parent_revision.doc", self.process_parent_revision_doc,
                       depends_on=[revision.metadata]),
            Datasource("parent_revision.metadata",
                       self.process_revision_metadata,
                       depends_on=[parent_revision_doc]),
            Datasource("parent_revision.text",
                       self.process_revision_text,
                       depends_on=[parent_revision_doc]),
            Datasource("previous_user_revision.doc",
                       self.process_previous_user_revision_doc,
                       depends_on=[revision.metadata]),
            Datasource("previous_user_revision.metadata",
                       self.process_revision_metadata,
                       depends_on=[previous_user_revision_doc]),
            Datasource("page_creation.doc",
                       self.process_page_creation_doc,
                       depends_on=[revision.metadata]),
            Datasource("page_creation.metadata",
                       self.process_revision_metadata,
                       depends_on=[page_creation_doc]),
            Datasource("user.doc",
                       self.process_user_doc,
                       depends_on=[revision.metadata]),
            Datasource("user.info",
                       self.process_user_info,
                       depends_on=[user_doc])
        ]}
        if self.language != None:
            local_context.update(self.language.context)

        local_context.update(context)
        local_cache.update(cache)

        super().__init__(local_context, local_cache)

    def extract(self, rev_ids, dependents, context=None, caches=None):
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
        caches = caches or {}
        context = dependencies.normalize_context(context)

        if hasattr(rev_ids, "__iter__"):
            return self._extract_many(rev_ids, dependents, context, caches)
        else:
            rev_id = rev_ids
            cache = caches
            return self._extract(rev_id, dependents, context, caches)

    def _extract_many(self, rev_ids, dependents, context, caches):
        all_dependents = set(dependencies.expand(dependents))

        # Prime caches
        extract_caches = defaultdict(dict)
        for rev_id in caches:
            extract_caches[rev_id].update(caches[rev_id])

        # Build up caches for data that can be queried in batch
        if revision.metadata in all_dependents or \
           revision.text in all_dependents:
            rev_ids_missing_data = [
                rid for rid in rev_ids
                if rid not in extract_caches or
                   revision.text not in extract_caches[rid] or
                   revision.metadata not in extract_caches[rid] or
                   revision_doc not in extract_caches[rid]
            ]
            rev_docs = self.get_rev_doc_map(rev_ids)

            for rev_id in rev_ids:
                extract_caches[rev_id][revision_doc] = rev_docs.get(rev_id)

            if parent_revision.metadata in all_dependents or \
               parent_revision.text in all_dependents:

                parent_ids = [r.get('parentid') for r in rev_docs.values()
                              if r.get('parentid', 0) > 0]

                parent_rev_docs = self.get_rev_doc_map(parent_ids)

                for rev_doc in rev_docs.values():
                    extract_caches[rev_doc['revid']][parent_revision_doc] = \
                            parent_rev_docs.get(rev_doc['parentid'])

            if user.info in all_dependents:
                user_texts = [r.get('user') for r in rev_docs.values()]
                user_docs = self.get_user_doc_map(user_texts)

                for rev_doc in rev_docs.values():
                    extract_caches[rev_doc['revid']][user_doc] = \
                            user_docs.get(rev_doc.get('user'))

        # Now extract dependent values one-by-one
        for rev_id in rev_ids:
            try:
                values = self._extract(rev_id, dependents, context=context,
                                       cache=extract_caches[rev_id])
                yield None, list(values)
            except Exception as e:
                yield e, None

    def _extract(self, rev_id, dependents, cache, context):
        extract_cache = {revision.id: rev_id}
        extract_cache.update(cache)
        return self.solve(dependents, context=context, cache=extract_cache)

    def get_namespace_map(self):
        logger.info("Requesting site info from the API")
        doc = self.session.site_info.query(
            properties={'general', 'namespaces', 'namespacealiases'}
        )

        return self.namespace_map_from_doc(doc)

    def get_rev_doc_map(self, rev_ids, props={'ids', 'user', 'timestamp',
                                              'userid', 'comment', 'content',
                                              'flags', 'size'}):
        if len(rev_ids) == 0: return {}
        logger.info("Batch requesting {0} revisions from the API" \
                    .format(len(rev_ids)))
        return {rd['revid']:rd
                for rd in self.session.revisions.query(
                    revids=rev_ids,
                    properties=props
                )}

    def get_user_doc_map(self, user_texts, props={'blockinfo', 'implicitgroups',
                                                  'groups', 'registration',
                                                  'emailable', 'editcount',
                                                  'gender'}):
        if len(user_texts) == 0: return {}
        logger.info("Batch requesting {0} users from the API" \
                    .format(len(user_texts)))
        return {ud['name']:ud
                for ud in self.session.users.query(
                    users=user_texts,
                    properties=props
                )}

    def process_revision_doc(self, rev_id):
        logger.info("Requesting a revision ({0}) from the API".format(rev_id))
        props = {'ids', 'user', 'timestamp', 'userid', 'comment',
                 'content', 'flags', 'size'}
        return self.session.revisions.get(rev_id=rev_id, properties=props)

    def process_parent_revision_doc(self, revision_metadata):
        props = {'ids', 'user', 'timestamp', 'userid', 'comment',
                 'content', 'flags', 'size'}
        if revision_metadata.parent_id is not None and \
            revision_metadata.parent_id > 0:
            rev_id = revision_metadata.parent_id
            try:
                logger.info("Requesting a parent revision ({0}) from the API" \
                            .format(rev_id))
                return self.session.revisions.get(
                    rev_id=rev_id,
                    properties=props
                )
            except KeyError:
                return None
        else:
            return None

    def process_previous_user_revision_doc(self, revision_metadata):
        if revision_metadata.user_text is not None:
            logger.info("Requesting previous user revision ({0}) from the API" \
                        .format(revision_metadata.user_text))
            docs = self.session.user_contribs.query(
                user={revision_metadata.user_text},
                properties={'ids', 'timestamp'},
                limit=1,
                direction="older",
                start=revision_metadata.timestamp-1
            )
            docs = list(docs)

            if len(docs) > 0:
                return docs[0]
            else:
                return None
        else:
            return None

    def process_page_creation_doc(self, revision_metadata):
        logger.info("Requesting page creation ({0}) from the API" \
                    .format(revision_metadata.page_id))
        docs = self.session.revisions.query(
            pageids={revision_metadata.page_id},
            direction="newer",
            limit=1,
            properties={'ids', 'user', 'timestamp', 'userid', 'comment',
                        'flags', 'size'}
        )
        docs = list(docs)

        if len(docs) == 1:
            return docs[0]
        else:
            raise RevisionDocumentNotFound(
                {'page_id': revision_metadata.page_id}
            )

    def process_user_doc(self, revision_metadata):
        logger.info("Requesting user info ({0}) from the API" \
                    .format(revision_metadata.user_text))
        user_docs = self.session.users.query(
            users={revision_metadata.user_text},
            properties={'blockinfo', 'implicitgroups', 'groups', 'registration',
                        'emailable', 'editcount', 'gender'}
        )

        user_docs = list(user_docs)

        if len(user_docs) >= 1:
            return user_docs[0]
        else:
            return None

    @classmethod
    def process_revision_metadata(cls, revision_doc):
        if revision_doc is None:
            raise RevisionDocumentNotFound()
        return cls.revision_metadata_from_doc(revision_doc)

    @classmethod
    def process_user_info(cls, user_doc):
        return cls.user_info_from_doc(user_doc)

    @classmethod
    def process_revision_text(cls, revision_doc):
        if revision_doc is None: return None
        return revision_doc.get('*', "")

    @classmethod
    def revision_metadata_from_doc(cls, rev_doc):
        if rev_doc is None: return None
        try:
            timestamp = Timestamp(rev_doc.get('timestamp'))
        except ValueError:
            timestamp = None

        return RevisionMetadata(rev_doc.get('revid'),
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

    @classmethod
    def user_info_from_doc(cls, user_doc):
        if user_doc is None: return None
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
            user_doc.get('blockid'),
            user_doc.get('blockedby'),
            user_doc.get('blockedbyid'),
            user_doc.get('blockedtimestamp'),
            user_doc.get('blockreason'),
            user_doc.get('blockexpiry')
        )

    @classmethod
    def namespace_map_from_doc(cls, site_doc):
        aliases = site_doc.get('namespacealiases', [])
        alias_map = {}
        for alias_doc in aliases:
            prev_list = alias_map.get(alias_doc['id'], [])
            prev_list.append(alias_doc['*'])
            alias_map[alias_doc['id']] = prev_list

        namespace_map = {}
        for ns_doc in site_doc.get('namespaces', {}).values():
            namespace = Namespace.from_doc(ns_doc, aliases=alias_map)
            namespace_map[namespace.id] = namespace

        return namespace_map

    @classmethod
    def from_config(cls, config, name, section_key="extractors"):
        section = config[section_key][name]
        session = api.Session(section['url'],
                              user_agent=section['user_agent'])

        language = Language.from_config(config, section['language'])

        return cls(session, language)
