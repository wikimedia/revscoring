import json

from pytest import raises

from revscoring.about import __version__
from revscoring.scoring.environment import Environment


def test_environment():
    env = Environment()

    print(env.format(formatting="str"))
    print(json.dumps(env.format(formatting="json"), indent=2))
    assert env.lookup(['revscoring_version']) == __version__
    env.check(raise_exception=True)


def test_env_error():
    with raises(RuntimeError):
        env = Environment()
        env['revscoring_version'] = "foo"
        print(json.dumps(env.format(formatting="json"), indent=2))
        env.check(raise_exception=True)
