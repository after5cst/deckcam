from deckcam import __version__
from pathlib import Path
import toml

_PARENT_DIR = Path(__file__).parent.parent


def test_version_matches_pyproject_toml():
    data = toml.load(_PARENT_DIR / "pyproject.toml")
    assert __version__ == data["tool"]["poetry"]["version"]
