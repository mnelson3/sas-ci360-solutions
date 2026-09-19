# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from sasci360solutions.identity_data.SendIdentityBridgeStatusMessage import (
    SendIdentityBridgeStatusMessage,
)


def test_send_identity_bridge_status_message_mode_development():
    mode = "development"
    file_name = "import_request_jobs_get_20200527160403"
    custom = SendIdentityBridgeStatusMessage(mode=mode)
    result = custom.run(file_name=file_name)
    print("result : {0}".format(result))
    assert result is None


def test_send_identity_bridge_status_message_mode_test():
    mode = "test"
    file_name = "import_request_jobs_get_20200527160332"
    custom = SendIdentityBridgeStatusMessage(mode=mode)
    result = custom.run(file_name=file_name)
    print("result : {0}".format(result))
    assert result is None


def test_send_identity_bridge_status_message_mode_production():
    mode = "production"
    custom = SendIdentityBridgeStatusMessage(mode=mode)
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None


def test_send_identity_bridge_status_message():
    custom = SendIdentityBridgeStatusMessage()
    result = custom.run()
    print("result : {0}".format(result))
    assert result is None
