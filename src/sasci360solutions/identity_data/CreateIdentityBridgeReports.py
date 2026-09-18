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
import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from sasci360apicore import connection, reporter

# from security import Security
# from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class CreateIdentityBridgeReports:

    def __init__(self, **kwargs):
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

        self.reporter = reporter.Reporter(root=root_path)

        # self.standard = Standard.Standard()
        # self.report_folder = self._standard.reports_path
        # self.external_gateway_path = self._standard.external_gateway_path
        # self.identity_bridge_table_id = self._standard.identity_bridge_table_id
        # self.secret_key = self._standard.secret_key
        # self.tenant_id = self._standard.tenant_id

        # self._gDirDataResponseImportRequestJobsGet = self._standard.gDirDataResponseImportRequestJobsGet
        # self._import_request_jobs_path = self._standard.import_request_jobs_path
        self.connection = connection.Connection()
        # self._security = Security.Security()

    def run(self, **kwargs):
        try:
            if "time_stamp" in kwargs:
                time_stamp_ = kwargs["time_stamp"]
            else:
                time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
                time_stamp_ = time_stamp.replace(":", "")

            self.refresh_data(time_stamp=time_stamp_)

            if self.__mode is not None:
                folder = "{0}{1}/".format(
                    self._gDirDataResponseImportRequestJobsGet, self.__mode
                )
            else:
                folder = "{0}{1}/".format(
                    self._gDirDataResponseImportRequestJobsGet, "development"
                )

            report_folder = self._report_folder
            table_id = self._identity_bridge_table_id
            file_name = "import_request_jobs_get_{}".format(time_stamp_)
            json_file = Path(
                "{0}{1}{2}{3}".format(root_path, folder, file_name, ".JSON")
            )
            csv_file = Path(
                "{0}{1}{2}{3}".format(root_path, report_folder, file_name, ".CSV")
            )

            counter = 1
            with open(json_file, "r", encoding="utf-8") as infile:
                result = json.load(infile)
                if result is not None:
                    for item in result["items"]:
                        if item["dataDescriptorId"] == table_id:
                            file_name_ = "{}".format(item["id"])
                            json_file_ = Path(
                                "{0}{1}{2}{3}".format(
                                    root_path, folder, file_name_, ".JSON"
                                )
                            )
                            record = []
                            with open(json_file_, "r", encoding="utf-8") as infile_:
                                result_ = json.load(infile_)
                                record.append(counter)
                                import_validation = result_["statusInfo"][
                                    "importValidation"
                                ]
                                item_status = import_validation["status"]
                                record.append(item_status)
                                item_start_time = import_validation["startTime"]
                                record.append(item_start_time)
                                item_end_time = import_validation["endTime"]
                                record.append(item_end_time)
                                item_messages = import_validation["messages"]
                                record.append(item_messages)
                                data_processing = result_["statusInfo"][
                                    "dataProcessing"
                                ]
                                item_status = data_processing["status"]
                                record.append(item_status)
                                item_start_time = data_processing["startTime"]
                                record.append(item_start_time)
                                item_end_time = data_processing["endTime"]
                                record.append(item_end_time)
                                item_messages = data_processing["messages"]
                                record.append(item_messages)
                                identity_processing = result_["statusInfo"][
                                    "identityProcessing"
                                ]
                                item_status = identity_processing["status"]
                                record.append(item_status)
                                item_start_time = identity_processing["startTime"]
                                record.append(item_start_time)
                                item_end_time = identity_processing["endTime"]
                                record.append(item_end_time)
                                item_messages = identity_processing["messages"]
                                record.append(item_messages)
                                record.append(str(json_file_))

                                if item_messages["info"] is not None:
                                    info_0 = item_messages["info"][
                                        "Total Number of Records Not Processed"
                                    ]
                                    record.append(info_0)
                                    info_1 = item_messages["info"][
                                        "Total Number of Identities Updated"
                                    ]
                                    record.append(info_1)
                                    info_2 = item_messages["info"][
                                        "Total Number of Identities Created"
                                    ]
                                    record.append(info_2)
                                    info_3 = item_messages["info"][
                                        "Total Number of Identities Rejected"
                                    ]
                                    record.append(info_3)
                                    info_4 = item_messages["info"][
                                        "Total Number of Records Processed"
                                    ]
                                    record.append(info_4)
                                if hasattr(result_, "failureOutputFiles"):
                                    failure_output_files = result_["failureOutputFiles"]
                                    failure_output_files_created_time_stamp = (
                                        failure_output_files["createdTimeStamp"]
                                    )
                                    record.append(
                                        failure_output_files_created_time_stamp
                                    )
                                    failure_output_files_expires_time_stamp = (
                                        failure_output_files["expiresTimeStamp"]
                                    )
                                    record.append(
                                        failure_output_files_expires_time_stamp
                                    )
                                    failure_output_files_http_method = (
                                        failure_output_files["httpMethod"]
                                    )
                                    record.append(failure_output_files_http_method)
                                    failure_output_files_version = failure_output_files[
                                        "version"
                                    ]
                                    record.append(failure_output_files_version)
                                    failure_output_files_signed_url = (
                                        failure_output_files["signedURL"]
                                    )
                                    record.append(failure_output_files_signed_url)

                                with open(
                                    csv_file, "a", newline="", encoding="utf-8"
                                ) as outfile:
                                    writer = csv.writer(outfile, dialect="excel")
                                    if counter == 1:
                                        record_header = [
                                            "No.",
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
                                            "Record Detail",
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
                                        writer.writerow(record_header)
                                    writer.writerow(record)
                                counter += 1
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def refresh_data(self, **kwargs):
        try:
            if "time_stamp" in kwargs:
                time_stamp_ = kwargs["time_stamp"]
            else:
                time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
                time_stamp_ = time_stamp.replace(":", "")

            if self.__mode is not None:
                folder = "{0}{1}/".format(
                    self._gDirDataResponseImportRequestJobsGet, self.__mode
                )
            else:
                folder = "{0}{1}/".format(
                    self._gDirDataResponseImportRequestJobsGet, "development"
                )

            external_gateway_path = self._external_gateway_path
            import_request_jobs_path = self._import_request_jobs_path
            secret_key = self._secret_key
            table_id = self._identity_bridge_table_id
            tenant_id = self._tenant_id
            token = self._security.generate_jwt(
                secret_key=secret_key, tenant_id=tenant_id
            )

            action = "GET"
            data = None
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(token),
            }
            params = None
            url = "https://{0}{1}?{2}".format(
                external_gateway_path, import_request_jobs_path, "start=0&limit=999"
            )
            result = self._connection.conn(
                action=action, data=data, headers=headers, params=params, url=url
            )
            file_name = "import_request_jobs_get_{}".format(time_stamp_)
            self._reporter.store_response(folder=folder, name=file_name, data=result)

            json_file = Path(
                "{0}{1}{2}{3}".format(root_path, folder, file_name, ".JSON")
            )

            with open(json_file, "r", encoding="utf-8") as outfile:
                _result = json.load(outfile)
                _url = None
                if _result is not None:
                    for item in _result["items"]:
                        if item["dataDescriptorId"] == table_id:
                            _id = item["id"]
                            for i in item["links"]:
                                if i["method"] == "GET":
                                    _url = i["href"]
                                    temporary_url = _url
                                    action = "GET"
                                    data = None
                                    headers = {
                                        "Accept": "application/json",
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer {0}".format(token),
                                    }
                                    params = None
                                    url = temporary_url
                                    result = self._connection.conn(
                                        action=action,
                                        data=data,
                                        headers=headers,
                                        params=params,
                                        url=url,
                                    )
                                    self._reporter.store_response(
                                        folder=folder,
                                        name="{}".format(_id),
                                        data=result,
                                    )
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return


if __name__ == "__main__":
    CreateIdentityBridgeReports.__init__(CreateIdentityBridgeReports())
