#!/usr/bin/env python3
#
# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from sasci360solutions.identity_data import (
    CreateIdentityBridgeReports,
    SendIdentityBridgeStatusMessage,
    SendIdentityBridgeSupportMessage,
    UploadIdentityBridgeData,
)
from standard import Standard


class CI360Main:
    """
    Orchestrates the identity-bridge reference workflow: upload a chain
    file to CI360, pull the resulting import-request-job status, and email
    the status/support distribution lists with the outcome.

    CI360 processes an import request job asynchronously in the background
    after upload; this class does not itself block waiting for that job to
    finish. The reference automation engine this replaces waited a fixed
    2-hour sleep between upload and polling -- that cadence decision
    belongs to whatever schedules calls into this class (cron, a
    long-running service loop using sasci360apicore.scheduler.Scheduler,
    etc.), not to a blocking sleep buried in application logic.
    """

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")
        self.logger = logging.getLogger(__name__)

        self.standard = kwargs.get("standard") or Standard(mode=self.mode)
        self.upload = kwargs.get("upload") or UploadIdentityBridgeData(
            mode=self.mode, standard=self.standard
        )
        self.create_reports = kwargs.get(
            "create_reports"
        ) or CreateIdentityBridgeReports(mode=self.mode, standard=self.standard)
        self.send_status = kwargs.get("send_status") or SendIdentityBridgeStatusMessage(
            mode=self.mode, standard=self.standard
        )
        self.send_support = kwargs.get(
            "send_support"
        ) or SendIdentityBridgeSupportMessage(mode=self.mode, standard=self.standard)

    def run_identity_bridge_cycle(self, file_name=None) -> bool:
        """
        Run one identity-bridge cycle.

        If file_name is given, uploads it, then pulls the import-request-job
        report for the identity-bridge table and emails the status list with
        the outcome (success or failure). If file_name is omitted, sends the
        "no chain file processed today" status message without contacting
        CI360.

        :param file_name: path to a chain CSV to upload; None to send a
            no-op status update instead.
        :return: True if the cycle (or the no-op update) completed
            successfully, False if the upload or any reported job failed.
        :rtype: bool
        """
        if file_name is None:
            return self.send_status.run()

        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

        uploaded = self.upload.run(file_name=file_name)
        if not uploaded:
            self.logger.error(
                "Upload failed for %s; not polling for job status", file_name
            )
            self.send_status.run(time_stamp=time_stamp, success=False)
            return False

        success = self.create_reports.run(time_stamp=time_stamp)
        self.send_status.run(time_stamp=time_stamp, success=success)
        return success

    def run_support_check(self) -> bool:
        """
        Run the independent, weekly support-message check: if a manually
        dropped identity-bridge change file is present, email it to SAS
        Technical Support.

        :return: True if a support email was sent, False otherwise.
        :rtype: bool
        """
        return self.send_support.run()

    def check_and_run(self) -> bool:
        """
        Check the configured drop location for a new chain file and, if
        present, move it out of the watched location and run a full
        identity-bridge cycle for it. This is the unit of work a
        scheduled/looping caller should invoke repeatedly; moving the file
        immediately (rather than after the cycle completes) means a new
        file can be dropped while this cycle's upload/report/notify steps
        are still in flight.

        :return: True if a cycle ran and succeeded, or if there was no file
            to process; False if a cycle ran and failed.
        :rtype: bool
        """
        source_path = Path(
            "{0}/{1}".format(self.standard.export_post_path, self.standard.export_file)
        )
        if not source_path.exists():
            return self.run_identity_bridge_cycle(file_name=None)

        time_stamp_ = datetime.now().strftime("%Y%m%d%H%M%S")
        export_file = self.standard.export_file
        archived_name = "{0}_{1}{2}".format(export_file[:-4], time_stamp_, ".CSV")
        archived_path = Path(
            "{0}{1}/{2}".format(
                self.upload.root_path, self.standard.export_path, archived_name
            )
        )
        archived_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, archived_path)
        os.remove(source_path)

        return self.run_identity_bridge_cycle(file_name=str(archived_path))


def main():
    """CLI entry point: run a single identity-bridge check-and-run cycle."""
    logging.basicConfig(level=logging.INFO)
    try:
        app = CI360Main()
        app.check_and_run()
    except Exception as e:
        logging.error(f"Application failed to run: {e}")
        raise


if __name__ == "__main__":
    main()
