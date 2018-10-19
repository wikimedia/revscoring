from ...datasources import Datasource
from ...errors import (EntityNotFound, PageNotFound, RevisionNotFound,
                       UserNotFound)
from .util import REV_PROPS, USER_PROPS


class RevDocById(Datasource):

    def __init__(self, revision, extractor):
        self.revision = revision
        self.extractor = extractor
        super().__init__(revision._name + ".doc", self.process,
                         depends_on=[revision.id, extractor.dependents])

    def process(self, rev_id, dependents):
        if rev_id == 0:
            return None

        rvprop = set(REV_PROPS)

        if self.revision.text in dependents:
            rvprop.add('content')

        rev_doc_map = self.extractor.get_rev_doc_map([rev_id], rvprop=rvprop)

        if rev_id not in rev_doc_map:
            raise RevisionNotFound(self.revision, rev_id=rev_id)
        else:
            return rev_doc_map[rev_id]


class PageCreationRevDoc(Datasource):

    def __init__(self, page, extractor):
        self.page = page
        self.extractor = extractor
        super().__init__(page.creation._name + ".doc", self.process,
                         depends_on=[page.id, extractor.dependents])

    def process(self, page_id, dependents):
        rvprop = set(REV_PROPS)

        if self.page.creation.text in dependents:
            rvprop.add('content')

        rev_doc = self.extractor.get_page_creation_doc(page_id, rvprop=rvprop)

        # If we didn't find a revision for page creation, this is bad.  Error.
        if rev_doc is None:
            raise PageNotFound(self.page, page_id)
        else:
            return rev_doc


class PropertySuggestionDoc(Datasource):

    def __init__(self, page, extractor):
        self.page = page
        self.extractor = extractor
        super().__init__(page.suggested.properties.name + ".doc", self.process,
                         depends_on=[page.title, extractor.dependents])

    def process(self, entity_id, dependents):

        property_suggestion_doc = \
            self.extractor.get_property_suggestion_doc(entity_id)

        # If we didn't find a revision for page creation, this is bad.  Error.
        if property_suggestion_doc is None:
            raise EntityNotFound(self.page, entity_id)
        else:
            return property_suggestion_doc


class UserInfoDoc(Datasource):

    def __init__(self, user, extractor):
        self.user = user
        self.extractor = extractor
        super().__init__(user.info._name + ".doc", self.process,
                         depends_on=[user.id, user.text])

    def process(self, user_id, user_text):
        if user_id == 0:
            return None  # Doesn't work for anons
        else:
            user_doc_map = self.extractor.get_user_doc_map([user_text],
                                                           usprop=USER_PROPS)

            if user_text not in user_doc_map:
                raise UserNotFound(self.user, user_text)
            else:
                return user_doc_map[user_text]


class LastUserRevDoc(Datasource):

    def __init__(self, revision, extractor):
        self.revision = revision
        self.extractor = extractor
        super().__init__(
            revision.user.last_revision._name + ".doc", self.process,
            depends_on=[revision.user.text, revision.timestamp,
                        extractor.dependents]
        )

    def process(self, user_text, rev_timestamp, dependents):
        ucprop = set(REV_PROPS)

        if self.revision.user.last_revision.text in dependents:
            ucprop.add('text')

        return self.extractor.get_last_user_revision(user_text, rev_timestamp,
                                                     ucprop=ucprop)
