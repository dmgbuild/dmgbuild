import plistlib
import subprocess
from pathlib import Path

import pytest

import dmgbuild
from dmgbuild.core import DMGError


def build_and_get_attached_entities(target, settings=None):
    """Build an empty image; return the entities attached while building."""
    events = []
    dmgbuild.build_dmg(str(target), "Test", settings=settings, callback=events.append)

    (attach,) = (
        event
        for event in events
        if event["type"] == "command::finished"
        and event.get("command") == "diskutil::attach"
    )
    return attach["output"]["system-entities"]


def test_sample_settings(tmp_path):
    """Test with the sample settings.py file."""
    target = tmp_path / "out.dmg"
    with pytest.warns(FutureWarning, match="license"):
        dmgbuild.build_dmg(
            str(target), "Test", str(Path(__file__).parent / "examples" / "settings.py")
        )

    assert target.exists()


def test_licenses_settings(tmp_path):
    """Test with the licenses settings.py file."""
    target = tmp_path / "out.dmg"
    with pytest.warns(FutureWarning, match="license"):
        dmgbuild.build_dmg(
            str(target),
            "Test",
            str(Path(__file__).parent / "licenses" / "settings.json"),
        )

    assert target.exists()


def test_sample_json(tmp_path):
    """Test with the sample settings.json file."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(
        str(target), "Test", str(Path(__file__).parent / "examples" / "settings.json")
    )

    assert target.exists()


def test_no_partition_map(tmp_path):
    """The image has no partition map."""
    entities = build_and_get_attached_entities(tmp_path / "out.dmg")

    # Without a partition map, the filesystem is attached as the whole disk.
    assert len(entities) == 1
    assert entities[0]["mount-point"]


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


def image_format(path):
    """Return the format code (e.g. "ULFO") of the disk image at path."""
    result = subprocess.run(
        ["/usr/sbin/diskutil", "image", "info", "--plist", str(path)],
        capture_output=True,
        check=True,
    )
    return plistlib.loads(result.stdout)["Image Format"]


def test_default_format(tmp_path):
    """By default, the image is compressed with lzfse."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(str(target), "Test")

    assert image_format(target) == "ULFO"


def test_explicit_format(tmp_path):
    """The format setting controls the format of the image."""
    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(str(target), "Test", settings={"format": "UDZO"})

    assert image_format(target) == "UDZO"


def test_unsupported_format(tmp_path):
    """A format diskutil can't produce fails before anything is created."""
    target = tmp_path / "out.dmg"
    with pytest.raises(DMGError, match="Unsupported format 'UDBZ'"):
        dmgbuild.build_dmg(str(target), "Test", settings={"format": "UDBZ"})

    assert list(tmp_path.iterdir()) == []


def test_unsupported_filesystem(tmp_path):
    """A filesystem other than HFS+ or APFS fails before anything is created."""
    target = tmp_path / "out.dmg"
    with pytest.raises(DMGError, match="Unsupported filesystem 'ExFAT'"):
        dmgbuild.build_dmg(str(target), "Test", settings={"filesystem": "ExFAT"})

    assert list(tmp_path.iterdir()) == []


def test_compression_level_ignored(tmp_path):
    """Setting compression_level warns, but the build still succeeds."""
    target = tmp_path / "out.dmg"
    with pytest.warns(UserWarning, match="compression_level"):
        dmgbuild.build_dmg(str(target), "Test", settings={"compression_level": 9})

    assert target.exists()


def test_apfs_no_partition_map(tmp_path):
    """An APFS image is created without a partition map."""
    entities = build_and_get_attached_entities(
        tmp_path / "out.dmg", settings={"filesystem": "APFS"}
    )

    content_hints = [entity.get("content-hint") for entity in entities]
    assert "GUID_partition_scheme" not in content_hints
    assert any(entity.get("mount-point") for entity in entities)


def test_no_hdiutil(tmp_path, monkeypatch):
    """Without a license, the build doesn't use the deprecated hdiutil."""
    real_run = subprocess.run
    tools = []

    def recording_run(args, *posargs, **kwargs):
        tools.append(args[0])
        return real_run(args, *posargs, **kwargs)

    monkeypatch.setattr(subprocess, "run", recording_run)

    target = tmp_path / "out.dmg"
    dmgbuild.build_dmg(str(target), "Test")

    assert target.exists()
    assert "/usr/sbin/diskutil" in tools
    assert "/usr/bin/hdiutil" not in tools


def test_output_overwritten(tmp_path):
    """An existing file at the output path is replaced."""
    target = tmp_path / "out.dmg"
    target.write_bytes(b"not a disk image")
    dmgbuild.build_dmg(str(target), "Test")

    assert image_format(target) == "ULFO"
