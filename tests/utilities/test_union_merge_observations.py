import json
import os.path
import tempfile

from revscoring.utilities.union_merge_observations import (
    main, union_merge_observations)


def test_union_merge():
    """Merge and inspect results.
    """
    observations = [
        {"rev_id": 101, "goodfaith": False, "damaging": True},
        {"rev_id": 101, "goodfaith": True, "damaging": True},
        {"rev_id": 102, "goodfaith": False, "damaging": False},
    ]
    expected = [
        {"rev_id": 101, "goodfaith": True, "damaging": True},
        {"rev_id": 102, "goodfaith": False, "damaging": False},
    ]
    result = union_merge_observations(observations, "rev_id")
    assert expected == list(result)


def test_union_cli():
    """Integration test to parse and run from a commandline.  This tests file
    loading.
    """
    # Get test fixtures.
    data_dir = os.path.dirname(__file__) + "/data"
    in_files = [
        data_dir + "/labeled_revisions.json",
        data_dir + "/labeled_foo.json",
    ]

    # Receive the output in a temporary file.
    (fh, out_file) = tempfile.mkstemp()

    # Do the union.
    argv = in_files + ["--output", out_file]
    main(argv)

    # Get results.
    with open(out_file, "r") as f:
        out_text = f.read()

    # Clean up test file :(  It would be better if a context manager could
    # ensure we don't abort before cleaning up.
    os.unlink(out_file)

    # Split result into lines.
    lines = out_text.strip().split("\n")

    # There should be six records.
    assert len(lines) == 6

    # If this counter is set to 1, it tells us that our row of interest was
    # present and not duplicated.
    count_merged = 0

    # Spot check a couple o' lines.
    for line in lines:
        obj = json.loads(line)
        if obj["rev_id"] == "16124458":
            assert obj == {"damaging": 0, "goodfaith": 1, "approved": 1,
                           "rev_id": "16124458"}
        if obj["rev_id"] == "16124390":
            assert obj == {"damaging": 0, "approved": 1, "goodfaith": 0,
                           "foo": 1, "rev_id": "16124390"}
            count_merged += 1

    assert count_merged == 1
