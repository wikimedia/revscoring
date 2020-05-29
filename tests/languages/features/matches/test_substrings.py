from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages.features import SubstringMatches

substrings = SubstringMatches(
    "english.idioms",
    ["blood", "bonding", "friends"],
)

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_regexes():
    cache = {p_text: "Blood runs in the family.",
             r_text: "Bonding connects friends and family."}

    assert (solve(substrings.revision.datasources.matches, cache=cache) ==
            ['bonding', 'friends'])

    assert solve(substrings.revision.matches, cache=cache) == 2

    assert (solve(substrings.revision.parent.datasources.matches, cache=cache) ==
            ['blood'])

    assert solve(substrings.revision.parent.matches, cache=cache) == 1

    diff = substrings.revision.diff

    assert solve(diff.datasources.matches_added,
                 cache=cache) == ['bonding', 'friends']

    assert solve(diff.matches_added, cache=cache) == 2.0

    assert solve(diff.datasources.matches_removed,
                 cache=cache) == ['blood']

    assert solve(diff.matches_removed, cache=cache) == 1.0

    assert (solve(diff.datasources.match_delta, cache=cache) ==
            {'bonding': 1, 'friends': 1, 'blood': -1})

    pd = solve(diff.datasources.match_prop_delta, cache=cache)
    assert pd.keys() == {'bonding', 'friends', 'blood'}

    assert round(pd['bonding'], 2) == 1.0
    assert round(pd['friends'], 2) == 1.0
    assert round(pd['blood'], 2) == -1.0

    assert round(solve(diff.match_delta_sum, cache=cache), 2) == 1
    assert round(solve(diff.match_prop_delta_sum, cache=cache), 2) == 1.0
