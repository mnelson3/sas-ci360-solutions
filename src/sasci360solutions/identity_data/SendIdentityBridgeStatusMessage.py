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
import smtplib
import sys
from datetime import datetime
from pathlib import Path

from sasci360apicore import communication

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class SendIdentityBridgeStatusMessage:

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")

        self._log_file = Path(
            "{0}{1}{2}".format(
                pkg_path, "/logs/", "custom_send_identity_bridge_status_message.log"
            )
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.standard = Standard(mode=self.mode)

        self.communication = communication.Communication(
            email_server=self.standard.email_server,
            email_server_login=self.standard.email_server_login,
            email_server_password=self.standard.email_server_password,
            email_server_port=self.standard.email_server_port,
        )

        self.email_msg_from = self.standard.email_msg_status_from
        self.email_msg_to = self.standard.email_msg_status_to
        self.report_path = self.standard.reports_path

    def run(self, **kwargs):
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            if "time_stamp" in kwargs:
                message = "A new chain file was processed today."
                time_stamp_ = kwargs["time_stamp"]
            else:
                message = "No chain file was processed today."
                time_stamp_ = time_stamp.replace(":", "")

            email_msg_from = self.email_msg_from
            email_msg_to = self.email_msg_to
            report_folder = self.report_path

            if "file_name" in kwargs:
                file_name = kwargs["file_name"]
                csv_file = Path(
                    "{0}{1}{2}{3}".format(root_path, report_folder, file_name, ".CSV")
                )
            else:
                file_name = "import_request_jobs_get_{}".format(time_stamp_)
                csv_file = Path(
                    "{0}{1}{2}{3}".format(root_path, report_folder, file_name, ".CSV")
                )

            msg_from = "SAS CI360 Automation Engine [DO-NOT-REPLY] <{0}>".format(
                email_msg_from
            )
            msg_to = email_msg_to
            msg_subject = "Daily Identity Bridge Update [{0}]".format(time_stamp)
            msg_body = message
            msg_attachment = csv_file

            self.communication.send_email(
                email_msg_from=msg_from,
                email_msg_to=msg_to,
                email_msg_subject=msg_subject,
                email_msg_body=msg_body,
                email_msg_attachment=msg_attachment,
            )
        except (smtplib.SMTPException, OSError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))


if __name__ == "__main__":
    SendIdentityBridgeStatusMessage.__init__(SendIdentityBridgeStatusMessage())
