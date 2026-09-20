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


class SendIdentityBridgeSupportMessage:
    """A weekly, file-triggered workflow: if a manually-dropped identity-bridge
    "change" file is present on disk, email it to SAS Technical Support for
    manual processing. Unrelated to the daily upload/report/status cycle's
    success or failure."""

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")

        self._log_file = Path(
            "{0}{1}{2}".format(
                pkg_path, "/logs/", "custom_send_identity_bridge_support_message.log"
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

    def run(self) -> bool:
        """
        Email a manually-dropped identity-bridge change file to SAS Technical
        Support, if one is present.

        :return: True if an email was sent, False if there was nothing to
            send or sending failed.
        :rtype: bool
        """
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            time_stamp_ = time_stamp.replace(":", "")

            export_change_file = self.standard.export_change_file
            export_post_path = self.standard.export_post_path
            export_folder = self.standard.export_path

            file_change_path = Path(
                "{0}/{1}".format(export_post_path, export_change_file)
            )

            if not file_change_path.exists():
                return False

            file_export_change = "{0}_{1}{2}".format(
                export_change_file[:-4], time_stamp_, ".CSV"
            )
            file_export_change_path = Path(
                "{0}{1}/{2}".format(self.root_path, export_folder, file_export_change)
            )
            file_export_change_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file_change_path, file_export_change_path)
            os.remove(file_change_path)

            msg_from = "SAS CI360 Solutions [DO-NOT-REPLY] <{0}>".format(
                self.standard.email_msg_support_from
            )
            msg_body = (
                "Environment: {0}\n"
                "Name: {1}\n"
                "Number: {2}\n"
                "Product: {3}\n"
                "URL: {4}\n"
                "User: {5}\n"
                "Time of attempt: {6}\n"
                "Issue: Please route this file to SAS Product Management and R&D "
                "for processing. The attached file is to be used to update the "
                "Identity Bridge Table to reflect the indicated changes to the "
                "corresponding IDs.".format(
                    self.standard.tenant_environment,
                    self.standard.tenant_name,
                    self.standard.tenant_number,
                    self.standard.tenant_product,
                    self.standard.tenant_url,
                    msg_from,
                    time_stamp,
                )
            )

            self.communication.send_email(
                email_msg_from=msg_from,
                email_msg_to="SAS Technical Support <{}>".format(
                    self.standard.email_msg_support_to
                ),
                email_msg_cc=self.standard.email_msg_support_cc,
                email_msg_subject="Identity Bridge Change Update [{0}]".format(
                    time_stamp
                ),
                email_msg_body=msg_body,
                email_msg_attachment=file_export_change_path,
            )
            return True
        except (OSError, smtplib.SMTPException) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return False


if __name__ == "__main__":
    SendIdentityBridgeSupportMessage.__init__(SendIdentityBridgeSupportMessage())
