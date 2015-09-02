from .. import site


def test_site():
    assert hasattr(site, "namespace_map")
