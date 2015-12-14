import os
import pickle

from nose.tools import eq_

from .. import parent_revision
from ....dependencies import solve
from ...parent_revision import text as parent_revision_text

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TOURING_TEXT = open(os.path.join(pwd, "alan_touring.json")).read()


def test_item_doc():
    solve(parent_revision.item_doc,
          cache={parent_revision_text: ALAN_TOURING_TEXT})

    eq_(pickle.loads(pickle.dumps(parent_revision.item_doc)),
        parent_revision.item_doc)


def test_item():
    solve(parent_revision.item,
          cache={parent_revision_text: ALAN_TOURING_TEXT})

    eq_(pickle.loads(pickle.dumps(parent_revision.item)), parent_revision.item)
