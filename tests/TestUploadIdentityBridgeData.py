# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import os

import pytest

from sasci360solutions.identity_data.UploadIdentityBridgeData import (
    UploadIdentityBridgeData,
)

requires_live_tenant = pytest.mark.skipif(
    not os.environ.get("CI360_RUN_LIVE_TESTS"),
    reason=(
        "UploadIdentityBridgeData.run() calls a live CI360 gateway and reads a "
        "real identity-bridge export file from disk; set CI360_RUN_LIVE_TESTS=1 "
        "with a populated config.ini to run it"
    ),
)


@requires_live_tenant
def test_upload_identity_bridge_data_mode_development():
    mode = "development"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


@requires_live_tenant
def test_upload_identity_bridge_data_mode_test():
    mode = "test"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


@requires_live_tenant
def test_upload_identity_bridge_data_mode_production():
    mode = "production"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


@requires_live_tenant
def test_upload_identity_bridge_data():
    custom = UploadIdentityBridgeData()
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None
