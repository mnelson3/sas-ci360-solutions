# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import csv
from types import SimpleNamespace
from unittest.mock import MagicMock

from sasci360solutions.identity_data.CreateIdentityBridgeReports import (
    CreateIdentityBridgeReports,
)


def _standard():
    return SimpleNamespace(
        algorithm="HS256",
        encoding="UTF-8",
        external_gateway_path="extapigwservice-test.ci360.sas.com",
        secret_key="example-secret-key",
        tenant_id="example-tenant-id",
        reports_path="/reports/",
        identity_bridge_table_id="table-1",
        gDirDataResponseImportRequestJobsGet="/data/response/import_request_jobs_get/",
    )


def _job_detail(status="Imported", failure=None):
    return {
        "id": "job-1",
        "dataDescriptorId": "table-1",
        "statusInfo": {
            "importValidation": {
                "status": status,
                "startTime": "t0",
                "endTime": "t1",
                "messages": {},
            },
            "dataProcessing": {
                "status": status,
                "startTime": "t0",
                "endTime": "t1",
                "messages": {},
            },
            "identityProcessing": {
                "status": status,
                "startTime": "t0",
                "endTime": "t1",
                "messages": {
                    "info": {
                        "Total Number of Records Not Processed": 0,
                        "Total Number of Identities Updated": 1,
                        "Total Number of Identities Created": 2,
                        "Total Number of Identities Rejected": 0,
                        "Total Number of Records Processed": 3,
                    }
                },
            },
        },
        "failureOutputFiles": failure,
    }


def test_job_succeeded_true_for_known_success_statuses():
    assert (
        CreateIdentityBridgeReports.job_succeeded(_job_detail(status="Imported"))
        is True
    )
    assert (
        CreateIdentityBridgeReports.job_succeeded(_job_detail(status="Completed"))
        is True
    )


def test_job_succeeded_false_for_unknown_status():
    assert (
        CreateIdentityBridgeReports.job_succeeded(_job_detail(status="Failed")) is False
    )


def test_job_succeeded_false_when_failure_output_files_present():
    detail = _job_detail(
        status="Imported", failure={"signedURL": "https://example.com/failure.csv"}
    )
    assert CreateIdentityBridgeReports.job_succeeded(detail) is False


def test_refresh_data_persists_and_returns_jobs():
    standard = _standard()
    client = MagicMock()
    client.get_import_request_jobs.return_value = {
        "items": [{"id": "job-1", "dataDescriptorId": "table-1"}]
    }
    reporter = MagicMock()

    custom = CreateIdentityBridgeReports(
        standard=standard, client=client, reporter=reporter
    )
    result = custom.refresh_data(time_stamp="20260101000000")

    assert result == {"items": [{"id": "job-1", "dataDescriptorId": "table-1"}]}
    client.get_import_request_jobs.assert_called_once_with(data_descriptor_id="table-1")
    reporter.save.assert_called_once()


def test_run_writes_csv_and_returns_true_on_success(tmp_path):
    standard = _standard()
    client = MagicMock()
    client.get_import_request_jobs.return_value = {
        "items": [{"id": "job-1", "dataDescriptorId": "table-1"}]
    }
    client.get_import_request_job.return_value = _job_detail(status="Imported")
    reporter = MagicMock()

    custom = CreateIdentityBridgeReports(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run(time_stamp="20260101000000")

    assert result is True
    csv_file = tmp_path / "reports" / "import_request_jobs_get_20260101000000.CSV"
    assert csv_file.exists()
    with open(csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0][0] == "No."
    assert rows[0][1] == "Outcome"
    assert rows[1][1] == "SUCCESS"


def test_run_returns_false_when_any_job_fails(tmp_path):
    standard = _standard()
    client = MagicMock()
    client.get_import_request_jobs.return_value = {
        "items": [
            {"id": "job-1", "dataDescriptorId": "table-1"},
            {"id": "job-2", "dataDescriptorId": "table-1"},
        ]
    }
    client.get_import_request_job.side_effect = [
        _job_detail(status="Imported"),
        _job_detail(status="Failed"),
    ]
    reporter = MagicMock()

    custom = CreateIdentityBridgeReports(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run(time_stamp="20260101000000")

    assert result is False
    csv_file = tmp_path / "reports" / "import_request_jobs_get_20260101000000.CSV"
    with open(csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    outcomes = [row[1] for row in rows[1:]]
    assert outcomes == ["SUCCESS", "FAILURE"]


def test_run_ignores_items_for_other_tables(tmp_path):
    standard = _standard()
    client = MagicMock()
    client.get_import_request_jobs.return_value = {
        "items": [{"id": "job-1", "dataDescriptorId": "some-other-table"}]
    }
    reporter = MagicMock()

    custom = CreateIdentityBridgeReports(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.run(time_stamp="20260101000000")

    assert result is True
    client.get_import_request_job.assert_not_called()


def test_run_returns_false_on_refresh_failure():
    from sasci360soldata.base import CI360DataConnectionError

    standard = _standard()
    client = MagicMock()
    client.get_import_request_jobs.side_effect = CI360DataConnectionError("boom")
    reporter = MagicMock()

    custom = CreateIdentityBridgeReports(
        standard=standard, client=client, reporter=reporter
    )
    result = custom.run(time_stamp="20260101000000")

    assert result is False
