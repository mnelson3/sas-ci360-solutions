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
    """Emails the identity-bridge status distribution list with the outcome of
    a cycle. Unlike the legacy implementation, the subject/recipients/body
    actually reflect whether the underlying jobs succeeded or failed."""

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

        self.root_path = kwargs.get("root_path", root_path)
        self.standard = kwargs.get("standard") or Standard(mode=self.mode)

        self.communication = kwargs.get("communication") or communication.Communication(
            email_server=self.standard.email_server,
            email_server_login=self.standard.email_server_login,
            email_server_password=self.standard.email_server_password,
            email_server_port=self.standard.email_server_port,
        )

        self.email_msg_from = self.standard.email_msg_status_from
        self.email_msg_to = self.standard.email_msg_status_to
        self.email_msg_support_cc = self.standard.email_msg_support_cc
        self.report_path = self.standard.reports_path

    def run(self, **kwargs) -> bool:
        """
        Send the identity-bridge status email.

        :keyword time_stamp: timestamp of the report this message covers; if
            omitted, no chain file is assumed to have been processed today.
        :keyword file_name: report file base name to attach, without
            extension; defaults to "import_request_jobs_get_<time_stamp>".
        :keyword success: bool, whether the underlying identity-bridge jobs
            succeeded. Defaults to True (a plain status update) when a
            time_stamp is given but success isn't specified, and is ignored
            when no time_stamp is given (nothing ran, so there's nothing to
            have failed).
        :return: True if the email was attempted (does not confirm SMTP
            delivery — Communication.send_email does not report that).
        :rtype: bool
        """
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")

            if "time_stamp" in kwargs:
                time_stamp_ = kwargs["time_stamp"]
                success = kwargs.get("success", True)
                if success:
                    message = "A new chain file was processed today and completed successfully."
                    subject_tag = "Success"
                else:
                    message = (
                        "A new chain file was processed today, but one or more "
                        "identity-bridge jobs failed. See the attached report for details."
                    )
                    subject_tag = "FAILURE"
            else:
                time_stamp_ = time_stamp.replace(":", "")
                success = True
                message = "No chain file was processed today."
                subject_tag = "Status"

            report_folder = self.report_path
            if "file_name" in kwargs:
                file_name = kwargs["file_name"]
            else:
                file_name = "import_request_jobs_get_{}".format(time_stamp_)
            csv_file = Path(
                "{0}{1}{2}{3}".format(self.root_path, report_folder, file_name, ".CSV")
            )

            msg_from = "SAS CI360 Solutions [DO-NOT-REPLY] <{0}>".format(
                self.email_msg_from
            )
            msg_to = self.email_msg_to
            msg_cc = None if success else self.email_msg_support_cc
            msg_subject = "Identity Bridge Update [{0}] [{1}]".format(
                subject_tag, time_stamp
            )

            send_kwargs = dict(
                email_msg_from=msg_from,
                email_msg_to=msg_to,
                email_msg_subject=msg_subject,
                email_msg_body=message,
                email_msg_attachment=csv_file,
            )
            if msg_cc:
                send_kwargs["email_msg_cc"] = msg_cc

            self.communication.send_email(**send_kwargs)
            return True
        except (smtplib.SMTPException, OSError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return False


if __name__ == "__main__":
    SendIdentityBridgeStatusMessage.__init__(SendIdentityBridgeStatusMessage())
