# -*- coding: utf-8 -*-
import dmgbuild
import pytest
import os

def test_sample_settings():
    """Test with the sample settings.py file."""
    dmgbuild.build_dmg('/tmp/out.dmg', 'Test', 'examples/settings.py')

    assert os.path.exists('/tmp/out.dmg')

def test_sample_json():
    """Test with the sample settings.json file."""
    dmgbuild.build_dmg('/tmp/out2.dmg', 'Test', 'examples/settings.json')

    assert os.path.exists('/tmp/out2.dmg')
