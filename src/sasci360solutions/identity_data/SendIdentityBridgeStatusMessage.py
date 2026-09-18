# Business Source License 1.1
#
# Note: on the Change Date below, this project automatically converts to the
# Change License, reproduced in full in LICENSE-CHANGE-LICENSE.txt.
#
# Parameters
#
# Licensor:             Nelson Grey LLC
# Licensed Work:        SAS CI360 Solutions
# Additional Use Grant: None
# Change Date:          2029-12-13
# Change License:       Apache License 2.0
#
# Terms
#
# The Licensor hereby grants you the right to copy, modify, create derivative
# works, redistribute, and make non-production use of the Licensed Work. The
# Licensor may make an Additional Use Grant, above, permitting limited
# production use.
#
# Effective on the Change Date, or the fourth anniversary of the first publicly
# available distribution of a specific version of the Licensed Work under this
# License, whichever comes first, the Licensor hereby grants you rights under
# the terms of the Change License, and the rights granted in the paragraph
# above terminate.
#
# If your use of the Licensed Work does not comply with the requirements
# currently in effect as described in this License, you must purchase a
# commercial license from the Licensor, its affiliated entities, or authorized
# resellers, or you must refrain from using the Licensed Work.
#
# All copies of the original and modified Licensed Work, and derivative works
# of the Licensed Work, are subject to this License. This License applies
# separately for each version of the Licensed Work and the Change Date may vary
# for each version of the Licensed Work released by Licensor.
#
# You must conspicuously display this License on each original or modified copy
# of the Licensed Work. If you receive the Licensed Work in original or
# modified form from a third party, the terms and conditions set forth in this
# License apply to your use of that work.
#
# Any use of the Licensed Work in violation of this License will automatically
# terminate your rights under this License for the current and all other
# versions of the Licensed Work.
#
# This License does not grant you any right in any trademark or logo of
# Licensor or its affiliates (provided that you may use a trademark or logo of
# Licensor as expressly required by this License).
#
# TO THE EXTENT PERMITTED BY APPLICABLE LAW, THE LICENSED WORK IS PROVIDED ON
# AN "AS IS" BASIS. LICENSOR HEREBY DISCLAIMS ALL WARRANTIES AND CONDITIONS,
# EXPRESS OR IMPLIED, INCLUDING (WITHOUT LIMITATION) WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, AND
# TITLE.
#
# MariaDB hereby grants you permission to use this License's text to license
# your works, and to refer to it using the trademark "Business Source License",
# as long as you comply with the Covenants of Licensor below.
#
# Covenants of Licensor
#
# In consideration of the right to use this License's text and the "Business
# Source License" name and trademark, Licensor covenants to MariaDB, a Delaware
# corporation, for the benefit of MariaDB and any other party that has
# contributed to the Licensed Work, to use best efforts to provide the Change
# License on the Change Date for each version of the Licensed Work, and to
# designate the Change License as "Apache License 2.0" or a later version of
# the Apache License.

# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Business Source License 1.1 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import logging
import os
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

    def __init__(self):
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

        self.communication = communication.Communication()

        self.standard = Standard.Standard()
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
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return


if __name__ == "__main__":
    SendIdentityBridgeStatusMessage.__init__(SendIdentityBridgeStatusMessage())
