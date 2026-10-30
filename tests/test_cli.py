import pytest

from dmgbuild import __version__
from dmgbuild.__main__ import main


def test_version(monkeypatch, capsys):
    """--version prints the program name and version, then exits cleanly."""
    monkeypatch.setattr("sys.argv", ["dmgbuild", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == f"dmgbuild {__version__}\n"
    assert captured.err == ""
