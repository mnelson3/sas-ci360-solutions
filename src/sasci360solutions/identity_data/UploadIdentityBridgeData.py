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
import shutil
import sys
from datetime import datetime
from pathlib import Path

from sasci360apicore import connection, reporter

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class UploadIdentityBridgeData:

    def __init__(self, **kwargs):
        self._log_file = Path(
            "{0}{1}{2}".format(
                pkg_path, "/logs/", "custom_upload_identity_bridge_data.log"
            )
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.connection = connection.Connection()
        self.reporter = reporter.Reporter(root=root_path)

        self.standard = Standard()
        self.export_file = self.standard.export_file
        self.export_path = self.standard.export_path
        self.export_post_path = self.standard.export_post_path
        self.external_gateway_path = self.standard.external_gateway_path
        self.secret_key = self.standard.secret_key
        self.tenant_id = self.standard.tenant_id

        self.gDirDataResponseFileTransferLocationPost = (
            self.standard.gDirDataResponseFileTransferLocationPost
        )
        self.file_transfer_location_path = self.standard.file_transfer_location_path

    def run(self, result=None, **kwargs):
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            time_stamp_ = time_stamp.replace(":", "")

            if self.mode is not None:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, self.mode
                )
            else:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, "development"
                )

            export_folder = self.export_path
            external_gateway_path = self.external_gateway_path
            file_transfer_location_path = self.file_transfer_location_path

            secret_key = self.secret_key
            tenant_id = self.tenant_id
            token = self.security.generate_jwt(
                secret_key=secret_key, tenant_id=tenant_id
            )

            action = "POST"
            data = None
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(token),
            }
            params = None
            url = "https://{0}{1}".format(
                external_gateway_path, file_transfer_location_path
            )
            result = self.connection.connect(
                action=action, data=data, headers=headers, params=params, url=url
            )
            self.reporter.store_response(
                folder=folder,
                name="file_transfer_location_post_{}".format(time_stamp_),
                data=result,
            )

            __signed_url = None
            if result is not None:
                __signed_url = result["signedURL"]
            temporary_url = __signed_url

            if "file_name" in kwargs:
                file_name = kwargs["file_name"]
                csv_file = Path("{0}".format(file_name))
            else:
                file_post_path = self._export_post_path
                file_export_path = Path("{0}{1}".format(root_path, self._export_path))
                file_export = self._export_file
                file_export_timestamp = "{0}_{1}{2}".format(
                    file_export[:-4], time_stamp_, ".CSV"
                )
                shutil.copy(
                    Path("{0}/{1}".format(file_post_path, file_export)),
                    Path("{0}/{1}".format(file_export_path, file_export_timestamp)),
                )
                file_name = "{0}_{1}".format(file_export[:-4], time_stamp_)
                csv_file = Path(
                    "{0}{1}{2}{3}".format(root_path, export_folder, file_name, ".CSV")
                )

            result = None
            action = "PUT"
            data = csv_file
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            params = None
            url = temporary_url
            result = self.connection.connect(
                action=action, data=data, headers=headers, params=params, url=url
            )
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return result


if __name__ == "__main__":
    UploadIdentityBridgeData.__init__(UploadIdentityBridgeData())
