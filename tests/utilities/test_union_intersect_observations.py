from revscoring.utilities.intersect_merge_observations import \
    intersect_merge_observations


def test_intersect_merge():
    """Merge and inspect results.
    """
    a = [
        {"rev_id": 101, "goodfaith": False, "damaging": True},
        {"rev_id": 102, "goodfaith": False, "damaging": False},
    ]
    b = [
        {"rev_id": 101, "goodfaith": True, "damaging": True}
    ]
    expected = [
        {"rev_id": 101, "goodfaith": True, "damaging": True}
    ]
    result = intersect_merge_observations([a, b], "rev_id")
    assert expected == list(result)
