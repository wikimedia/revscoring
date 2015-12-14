import os
import pickle

from nose.tools import eq_

from .. import revision
from ....dependencies import solve
from ...revision import text as revision_text

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TOURING_TEXT = open(os.path.join(pwd, "alan_touring.json")).read()


def test_item_doc():
    solve(revision.item_doc, cache={revision_text: ALAN_TOURING_TEXT})

    eq_(pickle.loads(pickle.dumps(revision.item_doc)), revision.item_doc)


def test_item():
    solve(revision.item, cache={revision_text: ALAN_TOURING_TEXT})

    eq_(pickle.loads(pickle.dumps(revision.item)), revision.item)
