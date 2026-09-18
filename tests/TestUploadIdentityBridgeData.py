# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from sasci360solutions.identity_data.UploadIdentityBridgeData import (
    UploadIdentityBridgeData,
)


def test_upload_identity_bridge_data_mode_development():
    mode = "development"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


def test_upload_identity_bridge_data_mode_test():
    mode = "test"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


def test_upload_identity_bridge_data_mode_production():
    mode = "production"
    custom = UploadIdentityBridgeData(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None


def test_upload_identity_bridge_data():
    custom = UploadIdentityBridgeData()
    result = custom.run()
    print("result : {0}".format(result))
    assert result is not None
