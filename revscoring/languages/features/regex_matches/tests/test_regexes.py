import pickle


from .....datasources import revision_oriented
from .....dependencies import solve
from ..regex_matches import RegexMatches

badwords = RegexMatches(
    "english.badwords",
    [r'\w*bad\w*', r'butts'],
    exclusions=['notabadword']
)
r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text

badwords_notbad = badwords.excluding(
    [r'notbad'], name=badwords._name + "_notbad")


def test_regexes():
    cache = {p_text: "This is notabadword.  There're bad words butts already.",
             r_text: "This is bad superbadword. There're bad words already."}

    assert (solve(badwords.revision.datasources.matches, cache=cache) ==
            ['bad', 'superbadword', 'bad'])
    assert solve(badwords.revision.matches, cache=cache) == 3
    assert (solve(badwords.revision.parent.datasources.matches, cache=cache) ==
            ['bad', 'butts'])
    assert solve(badwords.revision.parent.matches, cache=cache) == 2

    diff = badwords.revision.diff
    assert (solve(diff.datasources.matches_added, cache=cache) ==
            ['bad', 'superbadword'])
    assert solve(diff.matches_added, cache=cache) == 2
    assert (solve(diff.datasources.matches_removed, cache=cache) ==
            ['butts'])
    assert solve(diff.matches_removed, cache=cache) == 1

    assert (solve(diff.datasources.match_delta, cache=cache) ==
            {'bad': 1, 'superbadword': 1, 'butts': -1})
    pd = solve(diff.datasources.match_prop_delta, cache=cache)
    assert pd.keys() == {'bad', 'superbadword', 'butts'}
    assert round(pd['bad'], 2) == 0.50
    assert round(pd['superbadword'], 2) == 1
    assert round(pd['butts'], 2) == -1

    assert round(solve(diff.match_delta_sum, cache=cache), 2) == 1
    assert round(solve(diff.match_prop_delta_sum, cache=cache), 2) == 0.50

    cache = {r_text: "This is bad but also notbad."}
    assert (solve(badwords_notbad.revision.datasources.matches, cache=cache) ==
            ['bad'])


def test_pickling():
    assert (pickle.loads(pickle.dumps(badwords.revision.matches)) ==
            badwords.revision.matches)
    assert (pickle.loads(pickle.dumps(badwords.revision.parent.matches)) ==
            badwords.revision.parent.matches)

    assert (pickle.loads(pickle.dumps(badwords.revision.diff.matches_added)) ==
            badwords.revision.diff.matches_added)
    assert (pickle.loads(pickle.dumps(badwords.revision.diff.matches_removed)) ==
            badwords.revision.diff.matches_removed)

    assert (pickle.loads(pickle.dumps(badwords.revision.diff.matches_added)) ==
            badwords.revision.diff.matches_added)
    assert (pickle.loads(pickle.dumps(badwords.revision.diff.matches_removed)) ==
            badwords.revision.diff.matches_removed)
