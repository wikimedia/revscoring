from .datasource import Datasource
from .rev_doc import rev_doc
from .revision_metadata import revision_metadata


def process(session, revision_metadata):
    
    if revision_metadata.user_text is not None:
        docs = session.user_contribs.query(user={"EpochFail"},
                                          properties={'ids'},
                                          limit=1,
                                          direction="older",
                                          start="20140901010101")
        docs = list(docs)
        if len(docs) > 0:
            return rev_doc(docs[0]['revid'], session)
        else:
            return {}
    else:
        return {}

previous_user_rev_doc = Datasource("previous_user_rev_doc", process,
                                   depends_on=['session', revision_metadata])
