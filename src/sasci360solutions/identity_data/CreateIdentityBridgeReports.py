# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import csv
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from sasci360apicore import reporter
from sasci360soldata.base import CI360DataBase, CI360DataConfig, CI360DataError

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)

# Job status values CI360 is known to use for a completed, error-free stage.
# NOTE: this list reflects the values seen in this project's own reference
# fixtures/history, not SAS's own published enum of every possible status
# string; treat anything not in this set as "not a confirmed success" and
# adjust as real tenant responses are observed.
_SUCCESS_STATUSES = {"imported", "completed", "success", "processed"}


class CreateIdentityBridgeReports:
    """Pulls import-request-job status for the identity-bridge table from CI360
    (via the sol-data client) and writes it out as a CSV report, one row per
    job, flagging whether each job succeeded or failed."""

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")

        self._log_file = Path(
            "{0}{1}{2}".format(
                pkg_path, "/logs/", "custom_create_identity_bridge_reports.log"
            )
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.root_path = kwargs.get("root_path", root_path)
        self.standard = kwargs.get("standard") or Standard(mode=self.mode)
        self.reporter = kwargs.get("reporter") or reporter.Reporter(root=self.root_path)

        self.client = kwargs.get("client") or CI360DataBase(
            CI360DataConfig(
                algorithm=self.standard.algorithm,
                encoding=self.standard.encoding,
                host="https://{0}".format(self.standard.external_gateway_path),
                secret_key=self.standard.secret_key,
                tenant_id=self.standard.tenant_id,
            )
        )

        self.reports_path = self.standard.reports_path
        self.identity_bridge_table_id = self.standard.identity_bridge_table_id
        self.gDirDataResponseImportRequestJobsGet = (
            self.standard.gDirDataResponseImportRequestJobsGet
        )

    def _folder(self):
        mode = self.mode if self.mode is not None else "development"
        return "{0}{1}/".format(self.gDirDataResponseImportRequestJobsGet, mode)

    @staticmethod
    def job_succeeded(job_detail: dict) -> bool:
        """
        Determine whether a single import-request-job's fetched detail
        represents a successful (error-free) run.

        A job is treated as failed if CI360 attached failureOutputFiles, or
        if any of its three status stages is present and isn't a known
        success value. See the _SUCCESS_STATUSES caveat above.
        """
        if job_detail.get("failureOutputFiles"):
            return False

        status_info = job_detail.get("statusInfo") or {}
        for stage in ("importValidation", "dataProcessing", "identityProcessing"):
            status = (status_info.get(stage) or {}).get("status")
            if status and str(status).strip().lower() not in _SUCCESS_STATUSES:
                return False
        return True

    def run(self, **kwargs) -> bool:
        """
        Refresh import-request-job data for the identity-bridge table and
        write a CSV report.

        :keyword time_stamp: timestamp (YYYYMMDDHHMMSS) to namespace this
            run's report/response files with; defaults to now.
        :return: True if every matching job succeeded (or none matched),
            False if any job failed or the refresh itself raised.
        :rtype: bool
        """
        try:
            time_stamp_ = kwargs.get("time_stamp") or datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )

            jobs = self.refresh_data(time_stamp=time_stamp_)
            if jobs is None:
                return False

            report_folder = self.reports_path
            table_id = self.identity_bridge_table_id
            file_name = "import_request_jobs_get_{}".format(time_stamp_)
            csv_file = Path(
                "{0}{1}{2}{3}".format(self.root_path, report_folder, file_name, ".CSV")
            )

            counter = 0
            overall_success = True
            for item in jobs.get("items", []):
                if item.get("dataDescriptorId") != table_id:
                    continue
                job_detail = self.client.get_import_request_job(item["id"])
                self.reporter.save(
                    folder=self._folder(), name="{}".format(item["id"]), data=job_detail
                )
                counter += 1
                succeeded = self.job_succeeded(job_detail)
                overall_success = overall_success and succeeded
                self._write_item_record(job_detail, csv_file, counter, succeeded)

            return overall_success
        except (KeyError, OSError, CI360DataError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return False

    def _write_item_record(self, job_detail, csv_file, counter, succeeded):
        status_info = job_detail.get("statusInfo") or {}
        import_validation = status_info.get("importValidation") or {}
        data_processing = status_info.get("dataProcessing") or {}
        identity_processing = status_info.get("identityProcessing") or {}
        item_messages = identity_processing.get("messages") or {}
        info = item_messages.get("info") or {}
        failure_output_files = job_detail.get("failureOutputFiles") or {}

        record = [
            counter,
            "SUCCESS" if succeeded else "FAILURE",
            import_validation.get("status"),
            import_validation.get("startTime"),
            import_validation.get("endTime"),
            import_validation.get("messages"),
            data_processing.get("status"),
            data_processing.get("startTime"),
            data_processing.get("endTime"),
            data_processing.get("messages"),
            identity_processing.get("status"),
            identity_processing.get("startTime"),
            identity_processing.get("endTime"),
            item_messages,
            info.get("Total Number of Records Not Processed"),
            info.get("Total Number of Identities Updated"),
            info.get("Total Number of Identities Created"),
            info.get("Total Number of Identities Rejected"),
            info.get("Total Number of Records Processed"),
            failure_output_files.get("createdTimeStamp"),
            failure_output_files.get("expiresTimeStamp"),
            failure_output_files.get("httpMethod"),
            failure_output_files.get("version"),
            failure_output_files.get("signedURL"),
        ]

        csv_file.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_file, "a", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile, dialect="excel")
            if counter == 1:
                writer.writerow(
                    [
                        "No.",
                        "Outcome",
                        "importValidationStatus",
                        "importValidationStartTime",
                        "importValidationEndTime",
                        "importValidationMessages",
                        "dataProcessingStatus",
                        "dataProcessingStartTime",
                        "dataProcessingEndTime",
                        "dataProcessingMessages",
                        "identityProcessingStatus",
                        "identityProcessingStartTime",
                        "identityProcessingEndTime",
                        "identityProcessingMessages",
                        "Total Number of Records Not Processed",
                        "Total Number of Identities Updated",
                        "Total Number of Identities Created",
                        "Total Number of Identities Rejected",
                        "Total Number of Records Processed",
                        "createdTimeStamp",
                        "expiresTimeStamp",
                        "httpMethod",
                        "version",
                        "signedURL",
                    ]
                )
            writer.writerow(record)

    def refresh_data(self, **kwargs) -> Optional[dict]:
        """
        Fetch the current import-request-job summary for the identity-bridge
        table and persist the raw response as a JSON report.

        :keyword time_stamp: timestamp to namespace this run's response file
            with; defaults to now.
        :return: the parsed job-summary response, or None on failure.
        :rtype: dict
        """
        try:
            time_stamp_ = kwargs.get("time_stamp") or datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )

            jobs = self.client.get_import_request_jobs(
                data_descriptor_id=self.identity_bridge_table_id
            )
            self.reporter.save(
                folder=self._folder(),
                name="import_request_jobs_get_{}".format(time_stamp_),
                data=jobs,
            )
            return jobs
        except (KeyError, OSError, CI360DataError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return None


if __name__ == "__main__":
    CreateIdentityBridgeReports.__init__(CreateIdentityBridgeReports())
