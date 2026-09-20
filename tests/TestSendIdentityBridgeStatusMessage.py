# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from types import SimpleNamespace
from unittest.mock import MagicMock

from sasci360solutions.identity_data.SendIdentityBridgeStatusMessage import (
    SendIdentityBridgeStatusMessage,
)


def _standard():
    return SimpleNamespace(
        email_server="smtp.example.com",
        email_server_login="automation@example.com",
        email_server_password="changeme",
        email_server_port="465",
        email_msg_status_from="noreply@example.com",
        email_msg_status_to="admin@example.com",
        email_msg_support_cc="support@example.com",
        reports_path="/reports/",
    )


def test_send_status_message_no_file_processed():
    standard = _standard()
    communication = MagicMock()

    custom = SendIdentityBridgeStatusMessage(
        standard=standard, communication=communication
    )
    result = custom.run()

    assert result is True
    communication.send_email.assert_called_once()
    _, kwargs = communication.send_email.call_args
    assert "No chain file was processed today." in kwargs["email_msg_body"]
    assert "[Status]" in kwargs["email_msg_subject"]
    assert "email_msg_cc" not in kwargs


def test_send_status_message_success():
    standard = _standard()
    communication = MagicMock()

    custom = SendIdentityBridgeStatusMessage(
        standard=standard, communication=communication
    )
    result = custom.run(time_stamp="20260101000000", success=True)

    assert result is True
    _, kwargs = communication.send_email.call_args
    assert "completed successfully" in kwargs["email_msg_body"]
    assert "[Success]" in kwargs["email_msg_subject"]
    assert "email_msg_cc" not in kwargs


def test_send_status_message_failure_cc_s_support():
    standard = _standard()
    communication = MagicMock()

    custom = SendIdentityBridgeStatusMessage(
        standard=standard, communication=communication
    )
    result = custom.run(time_stamp="20260101000000", success=False)

    assert result is True
    _, kwargs = communication.send_email.call_args
    assert "one or more" in kwargs["email_msg_body"]
    assert "[FAILURE]" in kwargs["email_msg_subject"]
    assert kwargs["email_msg_cc"] == "support@example.com"


def test_send_status_message_smtp_failure_returns_false():
    import smtplib

    standard = _standard()
    communication = MagicMock()
    communication.send_email.side_effect = smtplib.SMTPException("boom")

    custom = SendIdentityBridgeStatusMessage(
        standard=standard, communication=communication
    )
    result = custom.run(time_stamp="20260101000000", success=True)

    assert result is False
