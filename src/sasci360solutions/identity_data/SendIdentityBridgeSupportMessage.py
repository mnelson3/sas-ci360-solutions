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

# Business Source License 1.1
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
import shutil
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
    __mode = None

    def __init__(self, **kwargs):
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

        if "mode" in kwargs:
            SendIdentityBridgeSupportMessage.__mode = kwargs["mode"]
        else:
            SendIdentityBridgeSupportMessage.__mode = None
        self.__mode = SendIdentityBridgeSupportMessage.__mode

        if self.__mode is not None:
            self._communication = communication.Communication(mode=self.__mode)
            self._standard = Standard.Standard(mode=self.__mode)
            self._secret_key = self._standard.secret_key_arr
            self._tenant_id = self._standard.tenant_id_arr
            self._export_path = self._standard.export_path_arr
            self._email_msg_from = self._standard.email_msg_support_from_arr
            self._email_msg_to = self._standard.email_msg_support_to_arr
            self._email_msg_cc = self._standard.email_msg_support_cc_arr
            self._tenant_environment = self._standard.tenant_environment_arr
            self._tenant_name = self._standard.tenant_name_arr
            self._tenant_number = self._standard.tenant_number_arr
            self._tenant_product = self._standard.tenant_product_arr
            self._tenant_url = self._standard.tenant_url_arr
            self._export_change_file = self._standard.export_change_file_arr
            self._export_post_path = self._standard.export_post_path_arr
        else:
            self._communication = communication.Communication()
            self._standard = Standard.Standard()
            self._secret_key = self._standard.secret_key
            self._tenant_id = self._standard.tenant_id
            self._export_path = self._standard.export_path
            self._email_msg_from = self._standard.email_msg_support_from
            self._email_msg_to = self._standard.email_msg_support_to
            self._email_msg_cc = self._standard.email_msg_support_cc
            self._tenant_environment = self._standard.tenant_environment
            self._tenant_name = self._standard.tenant_name
            self._tenant_number = self._standard.tenant_number
            self._tenant_product = self._standard.tenant_product
            self._tenant_url = self._standard.tenant_url
            self._export_change_file = self._standard.export_change_file
            self._export_post_path = self._standard.export_post_path

    def run(self):
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            time_stamp_ = time_stamp.replace(":", "")

            csv_file = None
            export_change_file = self._export_change_file
            export_post_path = self._export_post_path
            export_folder = self._export_path
            email_msg_from = self._email_msg_from
            email_msg_to = self._email_msg_to
            email_msg_cc = self._email_msg_cc
            tenant_environment = self._tenant_environment
            tenant_name = self._tenant_name
            tenant_number = self._tenant_number
            tenant_product = self._tenant_product
            tenant_url = self._tenant_url
            issue = (
                "Please route this file SAS CI360 Product Management and R&D for processing. "
                "The attached file is to be used to update the Identity Bridge Table to reflect "
                "the indicated changes to the corresponding IDs."
            )

            file_change_path = Path(
                "{0}/{1}".format(export_post_path, export_change_file)
            )

            if file_change_path.exists():
                file_export_change = "{0}_{1}{2}".format(
                    export_change_file[:-4], time_stamp_, ".CSV"
                )
                file_export_change_path = Path(
                    "{0}{1}/{2}".format(root_path, export_folder, file_export_change)
                )
                shutil.copy(file_change_path, file_export_change_path)

                if file_export_change_path.exists():
                    os.remove(file_change_path)
                csv_file = file_export_change_path

            if csv_file is not None:
                msg_from = "SAS CI360 Automation Engine [DO-NOT-REPLY] <{0}>".format(
                    email_msg_from
                )
                msg_to = "SAS Technical Support <{}>".format(email_msg_to)
                msg_cc = email_msg_cc
                msg_subject = "Identity Bridge Change Update [{0}]".format(time_stamp)
                msg_body = (
                    "Environment: {0}\n"
                    "Name: {1}\n"
                    "Number: {2}\n"
                    "Product: {3}\n"
                    "URL: {4}\n"
                    "User: {5}\n"
                    "Time of attempt: {6}\n"
                    "Issue: {7}".format(
                        tenant_environment,
                        tenant_name,
                        tenant_number,
                        tenant_product,
                        tenant_url,
                        msg_from,
                        time_stamp,
                        issue,
                    )
                )
                msg_attachment = csv_file

                self._communication.send_email(
                    email_msg_from=msg_from,
                    email_msg_to=msg_to,
                    email_msg_cc=msg_cc,
                    email_msg_subject=msg_subject,
                    email_msg_body=msg_body,
                    email_msg_attachment=msg_attachment,
                )
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return


if __name__ == "__main__":
    SendIdentityBridgeSupportMessage.__init__(SendIdentityBridgeSupportMessage())
