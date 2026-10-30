from pathlib import Path

import pytest

import dmgbuild
from dmgbuild.core import DMGError


def build_and_get_attached_entities(target, settings=None):
    """Build an empty image; return the entities hdiutil attached while building."""
    events = []
    dmgbuild.build_dmg(str(target), "Test", settings=settings, callback=events.append)

    (attach,) = (
        event
        for event in events
        if event["type"] == "command::finished"
        and event.get("command") == "hdiutil::attach"
    )
    return attach["output"]["system-entities"]


def test_sample_settings(tmp_path):
    """Test with the sample settings.py file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "examples" / "settings.py")
    )

    assert target.exists()


def test_licenses_settings(tmp_path):
    """Test with the licenses settings.py file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "licenses" / "settings.json")
    )

    assert target.exists()


def test_sample_json(tmp_path):
    """Test with the sample settings.json file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "examples" / "settings.json")
    )

    assert target.exists()


def test_default_layout(tmp_path):
    """By default, the image has no partition map."""
    entities = build_and_get_attached_entities(tmp_path / "out.dmg")

    # Without a partition map, the filesystem is attached as the whole disk.
    assert len(entities) == 1
    assert entities[0]["mount-point"]


def test_partitioned_layout(tmp_path):
    """A partition map can be requested with the layout setting."""
    entities = build_and_get_attached_entities(
        tmp_path / "out.dmg", settings={"layout": "GPTSPUD"}
    )

    content_hints = [entity.get("content-hint") for entity in entities]
    assert "GUID_partition_scheme" in content_hints


def test_copy_failure(tmp_path):
    """A file that can't be copied into the image fails the build."""
    payload = tmp_path / "payload.bin"
    payload.write_bytes(bytes(32 * 1024 * 1024))
    target = tmp_path / "out.dmg"

    # The payload is bigger than the image, so ditto runs out of space.
    with pytest.raises(DMGError, match="Unable to copy"):
        dmgbuild.build_dmg(
            str(target), "Test", settings={"size": "10m", "files": [str(payload)]}
        )

    assert not target.exists()
