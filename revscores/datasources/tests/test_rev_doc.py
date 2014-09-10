from nose.tools import eq_

from ..rev_doc import rev_doc


class FakeRevisions:
    
    def __init__(self, rev_doc):
        self.rev_doc = rev_doc
    
    def get(self, rev_id, *args, **kwargs):
        if self.rev_doc['revid'] == rev_id:
            return self.rev_doc
        else:
            raise KeyError(rev_id)

class FakeSession:
    
    def __init__(self, rev_doc):
        self.revisions = FakeRevisions(rev_doc)


def test_rev_doc():
    rev_id = 302
    doc = {'revid': rev_id, 'comment': "FOOBAR!"}
    session = FakeSession(doc)
    
    rd = rev_doc(rev_id, session)
    
    eq_(rd, doc)
