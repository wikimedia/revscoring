import io
import json
import os.path

from revscoring.utilities.union_merge_observations import DataUnion


def test_union():
    # Get test fixtures.
    data_dir = os.path.dirname(__file__) + "/data"
    in_files = [
        data_dir + "/labeled_revisions.json",
        data_dir + "/labeled_foo.json",
    ]

    # Receive the output as a string buffer.
    out_file = io.StringIO()

    # Do the union.
    DataUnion().union(in_files, out_file)

    # Split result into lines.
    lines = out_file.getvalue().strip().split("\n")

    # There should be six records.
    assert len(lines) == 6

    # If this counter is set to 1, it tells us that our row of interest was
    # present and not duplicated.
    count_merged = 0

    # Spot check a couple o' lines.
    for line in lines:
        obj = json.loads(line)
        if obj["rev_id"] == "16124458":
            assert obj == {"damaging": 0, "goodfaith": 1, "approved": 1, "rev_id": "16124458"}
        if obj["rev_id"] == "16124390":
            assert obj == {"damaging": 0, "approved": 1, "goodfaith": 0, "foo": 1, "rev_id": "16124390"}
            count_merged += 1

    assert count_merged == 1
