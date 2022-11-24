from pathlib import Path

import dmgbuild


def test_sample_settings(tmp_path):
    """Test with the sample settings.py file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "examples" / "settings.py")
    )

    assert target.exists()


def test_sample_json(tmp_path):
    """Test with the sample settings.json file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "examples" / "settings.json")
    )

    assert target.exists()
