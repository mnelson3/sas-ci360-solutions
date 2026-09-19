# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from sasci360solutions.identity_data.CreateIdentityBridgeReports import (
    CreateIdentityBridgeReports,
)


def test_create_identity_bridge_reports_mode_development():
    mode = "development"
    custom = CreateIdentityBridgeReports(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None


def test_create_identity_bridge_reports_mode_test():
    mode = "test"
    custom = CreateIdentityBridgeReports(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None


def test_create_identity_bridge_reports_mode_production():
    mode = "production"
    custom = CreateIdentityBridgeReports(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None


def test_create_identity_bridge_reports():
    custom = CreateIdentityBridgeReports()
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None
