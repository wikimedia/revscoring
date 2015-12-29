import pickle

from nose.tools import eq_

from .....datasources import revision_oriented
from .....dependencies import solve
from ..regex_matches import RegexMatches

badwords = RegexMatches(
    "english.badwords",
    [r'\w*bad\w*', r'butts'],

)
r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_regexes():
    cache = {p_text: "This is good.  There're bad words butts already.",
             r_text: "This is bad superbadword. There're bad words already."}

    eq_(solve(badwords.revision.datasources.matches, cache=cache),
        ['bad', 'superbadword', 'bad'])
    eq_(solve(badwords.revision.matches, cache=cache), 3)
    eq_(solve(badwords.revision.parent.datasources.matches, cache=cache),
        ['bad', 'butts'])
    eq_(solve(badwords.revision.parent.matches, cache=cache), 2)

    diff = badwords.revision.diff
    eq_(solve(diff.datasources.matches_added, cache=cache),
        ['bad', 'superbadword'])
    eq_(solve(diff.matches_added, cache=cache), 2)
    eq_(solve(diff.datasources.matches_removed, cache=cache),
        ['butts'])
    eq_(solve(diff.matches_removed, cache=cache), 1)

    eq_(solve(diff.datasources.match_delta, cache=cache),
        {'bad': 1, 'superbadword': 1, 'butts': -1})
    pd = solve(diff.datasources.match_prop_delta, cache=cache)
    eq_(pd.keys(), {'bad', 'superbadword', 'butts'})
    eq_(round(pd['bad'], 2), 0.50)
    eq_(round(pd['superbadword'], 2), 1)
    eq_(round(pd['butts'], 2), -1)

    eq_(round(solve(diff.match_delta_sum, cache=cache), 2), 1)
    eq_(round(solve(diff.match_prop_delta_sum, cache=cache), 2), 0.50)


def test_pickling():
    eq_(pickle.loads(pickle.dumps(badwords.revision.matches)),
        badwords.revision.matches)
    eq_(pickle.loads(pickle.dumps(badwords.revision.parent.matches)),
        badwords.revision.parent.matches)

    eq_(pickle.loads(pickle.dumps(badwords.revision.diff.matches_added)),
        badwords.revision.diff.matches_added)
    eq_(pickle.loads(pickle.dumps(badwords.revision.diff.matches_removed)),
        badwords.revision.diff.matches_removed)

    eq_(pickle.loads(pickle.dumps(badwords.revision.diff.matches_added)),
        badwords.revision.diff.matches_added)
    eq_(pickle.loads(pickle.dumps(badwords.revision.diff.matches_removed)),
        badwords.revision.diff.matches_removed)
