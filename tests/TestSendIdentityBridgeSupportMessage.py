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

from sasci360solutions.identity_data.SendIdentityBridgeSupportMessage import (
    SendIdentityBridgeSupportMessage,
)


def _standard(tmp_path, with_change_file=True):
    export_path = tmp_path / "export"
    export_post_path = tmp_path / "post"
    export_path.mkdir()
    export_post_path.mkdir()
    if with_change_file:
        (export_post_path / "export_change.csv").write_text("id\n1\n")

    return SimpleNamespace(
        email_server="smtp.example.com",
        email_server_login="automation@example.com",
        email_server_password="changeme",
        email_server_port="465",
        export_change_file="export_change.csv",
        export_post_path=str(export_post_path),
        export_path="/{0}/".format(export_path.name),
        email_msg_support_from="support@example.com",
        email_msg_support_to="support@example.com",
        email_msg_support_cc="cc@example.com",
        tenant_environment="test",
        tenant_name="Example Tenant",
        tenant_number="000000",
        tenant_product="SAS Customer Intelligence 360",
        tenant_url="https://example.com",
    )


def test_sends_email_when_change_file_present(tmp_path):
    standard = _standard(tmp_path, with_change_file=True)
    communication = MagicMock()

    custom = SendIdentityBridgeSupportMessage(
        standard=standard, communication=communication, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is True
    communication.send_email.assert_called_once()
    _, kwargs = communication.send_email.call_args
    assert "SAS Technical Support" in kwargs["email_msg_to"]
    assert kwargs["email_msg_cc"] == "cc@example.com"
    assert "Example Tenant" in kwargs["email_msg_body"]

    # the original drop-location file should have been moved, not left in place
    assert not (tmp_path / "post" / "export_change.csv").exists()


def test_no_email_when_change_file_absent(tmp_path):
    standard = _standard(tmp_path, with_change_file=False)
    communication = MagicMock()

    custom = SendIdentityBridgeSupportMessage(
        standard=standard, communication=communication, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is False
    communication.send_email.assert_not_called()


def test_smtp_failure_returns_false(tmp_path):
    import smtplib

    standard = _standard(tmp_path, with_change_file=True)
    communication = MagicMock()
    communication.send_email.side_effect = smtplib.SMTPException("boom")

    custom = SendIdentityBridgeSupportMessage(
        standard=standard, communication=communication, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is False
