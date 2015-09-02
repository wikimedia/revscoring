from .. import previous_user_revision


def test_previous_user_revision():
    assert hasattr(previous_user_revision, "metadata")
