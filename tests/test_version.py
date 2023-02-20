import toml

import corpus_pax


def test_version():
    assert (
        toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        == corpus_pax.__version__
    )
