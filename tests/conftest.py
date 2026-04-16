"""Shared test fixtures."""

import json
import os
import tempfile
from pathlib import Path

import pytest


SAMPLE_JSON = '{"name": "konvert", "version": "0.1.0", "features": ["json", "yaml"]}'
SAMPLE_YAML = "name: konvert\nversion: 0.1.0\nfeatures:\n  - json\n  - yaml\n"
SAMPLE_TOML = 'name = "konvert"\nversion = "0.1.0"\nfeatures = ["json", "yaml"]\n'
SAMPLE_CSV = "name,version,feature\nkonvert,0.1.0,json\nkonvert,0.1.0,yaml\n"
SAMPLE_XML = '<root><name>konvert</name><version>0.1.0</version></root>'
SAMPLE_INI = "[metadata]\nname = konvert\nversion = 0.1.0\n"
SAMPLE_ENV = 'NAME=konvert\nVERSION="0.1.0"\n'


@pytest.fixture
def sample_json():
    return SAMPLE_JSON


@pytest.fixture
def sample_yaml():
    return SAMPLE_YAML


@pytest.fixture
def sample_toml():
    return SAMPLE_TOML


@pytest.fixture
def sample_csv():
    return SAMPLE_CSV


@pytest.fixture
def sample_xml():
    return SAMPLE_XML


@pytest.fixture
def sample_ini():
    return SAMPLE_INI


@pytest.fixture
def sample_env():
    return SAMPLE_ENV


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def json_file(tmp_dir):
    p = tmp_dir / "sample.json"
    p.write_text(SAMPLE_JSON, encoding="utf-8")
    return p


@pytest.fixture
def yaml_file(tmp_dir):
    p = tmp_dir / "sample.yaml"
    p.write_text(SAMPLE_YAML, encoding="utf-8")
    return p


@pytest.fixture
def toml_file(tmp_dir):
    p = tmp_dir / "sample.toml"
    p.write_text(SAMPLE_TOML, encoding="utf-8")
    return p
