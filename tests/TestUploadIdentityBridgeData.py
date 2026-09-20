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

from sasci360solutions.identity_data.UploadIdentityBridgeData import (
    UploadIdentityBridgeData,
)


def _standard(tmp_path):
    export_path = tmp_path / "export"
    export_post_path = tmp_path / "post"
    export_path.mkdir()
    export_post_path.mkdir()
    (export_post_path / "export.csv").write_text("id,email\n1,a@example.com\n")

    return SimpleNamespace(
        algorithm="HS256",
        encoding="UTF-8",
        external_gateway_path="extapigwservice-test.ci360.sas.com",
        secret_key="example-secret-key",
        tenant_id="example-tenant-id",
        export_file="export.csv",
        export_path="/{0}/".format(export_path.name),
        export_post_path=str(export_post_path),
        gDirDataResponseFileTransferLocationPost="/data/response/file_transfer_location_post/",
    )


def test_upload_identity_bridge_data_success(tmp_path):

    standard = _standard(tmp_path)
    client = MagicMock()
    client.create_file_transfer_location.return_value = {
        "signedURL": "https://example.com/signed"
    }
    client.upload_to_signed_url.return_value = True
    reporter = MagicMock()

    custom = UploadIdentityBridgeData(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is True
    client.create_file_transfer_location.assert_called_once()
    client.upload_to_signed_url.assert_called_once()
    args, kwargs = client.upload_to_signed_url.call_args
    assert args[0] == "https://example.com/signed"
    reporter.save.assert_called_once()


def test_upload_identity_bridge_data_explicit_file(tmp_path):

    csv_file = tmp_path / "chain.csv"
    csv_file.write_text("id\n1\n")

    standard = _standard(tmp_path)
    client = MagicMock()
    client.create_file_transfer_location.return_value = {
        "signedURL": "https://example.com/signed"
    }
    client.upload_to_signed_url.return_value = True
    reporter = MagicMock()

    custom = UploadIdentityBridgeData(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run(file_name=str(csv_file))

    assert result is True
    args, kwargs = client.upload_to_signed_url.call_args
    assert args[1] == str(csv_file)


def test_upload_identity_bridge_data_no_signed_url(tmp_path):

    standard = _standard(tmp_path)
    client = MagicMock()
    client.create_file_transfer_location.return_value = {}
    reporter = MagicMock()

    custom = UploadIdentityBridgeData(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is False
    client.upload_to_signed_url.assert_not_called()


def test_upload_identity_bridge_data_client_error(tmp_path):
    from sasci360soldata.base import CI360DataConnectionError

    standard = _standard(tmp_path)
    client = MagicMock()
    client.create_file_transfer_location.side_effect = CI360DataConnectionError("boom")
    reporter = MagicMock()

    custom = UploadIdentityBridgeData(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run()

    assert result is False
