# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
"""
standard.Standard reads config/config.ini relative to a module-level
root_path computed at import time. Every test here monkeypatches that
root_path to an empty tmp_path (no config/config.ini present), so these
tests exercise the documented "safe fallback defaults" behavior (NFR-6)
deterministically, regardless of whether the machine running them has a
real config.ini checked out locally.
"""
import configparser

import pytest

import standard as standard_module
from standard import Standard

# One (arr-backed property, private bare attr, private arr attr) triple per
# _by_mode-delegating property, so every property getter's single line gets
# called and verified against the same by-mode logic, instead of writing an
# near-identical test per property.
BY_MODE_PROPERTIES = [
    (
        "email_msg_support_from",
        "_email_msg_support_from",
        "_email_msg_support_from_arr",
    ),
    ("email_msg_support_to", "_email_msg_support_to", "_email_msg_support_to_arr"),
    ("email_msg_support_cc", "_email_msg_support_cc", "_email_msg_support_cc_arr"),
    ("export_file", "_export_file", "_export_file_arr"),
    ("export_change_file", "_export_change_file", "_export_change_file_arr"),
    ("secret_key", "_secret_key", "_secret_key_arr"),
    ("tenant_id", "_tenant_id", "_tenant_id_arr"),
    ("export_path", "_export_path", "_export_path_arr"),
    ("export_post_path", "_export_post_path", "_export_post_path_arr"),
    ("external_gateway_path", "_external_gateway_path", "_external_gateway_path_arr"),
    ("tenant_environment", "_tenant_environment", "_tenant_environment_arr"),
    ("tenant_name", "_tenant_name", "_tenant_name_arr"),
    ("tenant_number", "_tenant_number", "_tenant_number_arr"),
    ("tenant_product", "_tenant_product", "_tenant_product_arr"),
    ("tenant_url", "_tenant_url", "_tenant_url_arr"),
]

# The "_arr" property variants delegate _by_mode(arr, arr) - same arr value
# on both sides, so the mode selection still runs but bare and arr coincide.
BY_MODE_ARR_PROPERTIES = [name + "_arr" for name, _, _ in BY_MODE_PROPERTIES]


@pytest.fixture
def empty_config_root(tmp_path, monkeypatch):
    monkeypatch.setattr(standard_module, "root_path", str(tmp_path))
    return tmp_path


def test_init_uses_fallback_defaults_when_no_config_file(empty_config_root):
    config = Standard()

    assert config.email_msg_status_from == "noreply@example.com"
    assert config.algorithm == "HS256"
    assert config.encoding == "UTF-8"
    assert config.identity_bridge_table_id == "changeme"
    assert config.file_transfer_location_path == "/marketingData/fileTransferLocation"
    assert config.import_request_jobs_path == "/marketingData/importRequestJobs"
    assert config.reports_path == "/reports/"


def test_init_reads_values_from_a_real_config_file(empty_config_root):
    config_dir = empty_config_root / "config"
    config_dir.mkdir()
    (config_dir / "config.ini").write_text(
        "[SETTINGS]\nalgorithm = HS512\n\n[EMAIL]\nemail_msg_status_from = ops@example.com\n"
    )

    config = Standard()

    assert config.algorithm == "HS512"
    assert config.email_msg_status_from == "ops@example.com"


def test_by_mode_returns_bare_value_when_arr_is_empty(empty_config_root):
    config = Standard()
    assert config._by_mode("", "bare-value") == "bare-value"


@pytest.mark.parametrize(
    "mode,expected",
    [("development", "dev"), ("test", "test-val"), ("production", "prod")],
)
def test_by_mode_selects_value_for_each_mode(empty_config_root, mode, expected):
    config = Standard(mode=mode)
    assert config._by_mode("dev,test-val,prod", "bare-value") == expected


def test_by_mode_returns_bare_value_for_unrecognized_mode(empty_config_root):
    config = Standard(mode="staging")
    assert config._by_mode("dev,test-val,prod", "bare-value") == "bare-value"


def test_by_mode_returns_bare_value_when_no_mode_given(empty_config_root):
    config = Standard()
    assert config._by_mode("dev,test-val,prod", "bare-value") == "bare-value"


def test_by_mode_returns_bare_value_when_index_out_of_range(empty_config_root):
    config = Standard(mode="production")
    # only 2 values for a mode order where "production" is index 2
    assert config._by_mode("dev,test-val", "bare-value") == "bare-value"


def test_get_instance_returns_a_singleton(empty_config_root):
    Standard._instance = None
    try:
        first = Standard.get_instance()
        second = Standard.get_instance()
        assert first is second
    finally:
        Standard._instance = None


def test_plain_getter_methods(empty_config_root):
    config = Standard()

    assert config.delimiter() == ","
    assert config.flag_test_report() is True
    assert config.suppression_email_domain_list() == []
    assert config.suppression_form_name_list() == []
    assert config.tables_path() == "/marketingData/tables"


@pytest.mark.parametrize("prop_name,bare_attr,arr_attr", BY_MODE_PROPERTIES)
def test_by_mode_property_delegates_to_by_mode(
    empty_config_root, prop_name, bare_attr, arr_attr
):
    config = Standard(mode="test")
    setattr(config, bare_attr, "bare-fallback")
    setattr(config, arr_attr, "dev-val,test-val,prod-val")

    assert getattr(config, prop_name) == "test-val"


@pytest.mark.parametrize("prop_name", BY_MODE_ARR_PROPERTIES)
def test_by_mode_arr_property_returns_bare_when_unset(empty_config_root, prop_name):
    config = Standard()
    assert getattr(config, prop_name) == ""


def test_config_file_path_is_relative_to_root_path(empty_config_root, monkeypatch):
    real_read = configparser.ConfigParser.read
    seen_paths = []

    def spy_read(self, filenames, encoding=None):
        seen_paths.append(str(filenames))
        return real_read(self, filenames, encoding=encoding)

    monkeypatch.setattr(configparser.ConfigParser, "read", spy_read)

    Standard()

    assert any(str(empty_config_root) in p for p in seen_paths)
