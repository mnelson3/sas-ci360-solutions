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
import json
import sys
import time
from pathlib import Path

from connection import Connection
from custom import BuildEmailData, root_path
from log import Log

from standard import CleanData, CreateData, DownloadEntity, Standard

_log_file_ = Path(root_path + Standard.gDirLog + "custom-download_discover.log")
_log_ = Log.Log.get_instance()
_log_.log_file(_log_file_)
logger = _log_.logging()


class DownloadDiscover:
    def __init__(self, **kwargs):
        standard = Standard.Standard.get_instance()

        self._flag_test_report = standard.flag_test_report()

        if "duration" in kwargs:
            self._duration = kwargs["duration"]
        if "end_date" in kwargs:
            self._end_date = kwargs["end_date"]
        if "end_date_time" in kwargs:
            self._end_date_time = kwargs["end_date_time"]
        if "end_time" in kwargs:
            self._end_time = kwargs["end_time"]
        if "report_name" in kwargs:
            self._report_name = kwargs["report_name"]
        if "start_date" in kwargs:
            self._start_date = kwargs["start_date"]
        if "start_date_time" in kwargs:
            self._start_date_time = kwargs["start_date_time"]
        if "start_time" in kwargs:
            self._start_time = kwargs["start_time"]

    def duration(self, value=None):
        if value:
            self._duration = value
        try:
            if isinstance(self._duration, str):
                return int(self._duration)
            return self._duration
        except (AttributeError, Exception) as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def end_date(self, value=None):
        if value:
            self._end_date = value
        try:
            return self._end_date
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def end_date_time(self, value=None):
        if value:
            self._end_date_time = value
        try:
            return self._end_date_time
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def end_time(self, value=None):
        if value:
            self._end_time = value
        try:
            return self._end_time
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def report_name(self, value=None):
        if value:
            self._report_name = value
        try:
            return self._report_name
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def start_date(self, value=None):
        if value:
            self._start_date = value
        try:
            return self._start_date
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def start_date_time(self, value=None):
        if value:
            self._start_date_time = value
        try:
            return self._start_date_time
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def start_time(self, value=None):
        if value:
            self._start_time = value
        try:
            return self._start_time
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def run(self):
        try:
            flag_test_report = self._flag_test_report
            duration = self.duration()
            end_date_time = self.end_date_time()
            report_name = self.report_name()
            start_date_time = self.start_date_time()
            report_date = start_date_time
            # track start time
            run_start = time.time()
            # track get download URL request time
            get_urls_start = time.time()
            connection = Connection.Connection.get_instance()
            connection.duration(duration)
            connection.end_date_time(end_date_time)
            connection.report_name(report_name)
            connection.start_date_time(start_date_time)
            response = connection.get_discover()
            # track get download URL request time
            get_urls_end = time.time()
            get_urls_duration = round((get_urls_end - get_urls_start), 2)
            logger.info(
                msg="getDownloadUrl request duration: "
                + str(get_urls_duration)
                + " seconds"
            )
            json_data = json.loads(response)
            # track json response for debugging purpose into a file

            response_file = Path(root_path + Standard.gDsDscConfig + "response.json")
            with open(file=response_file, mode="w", encoding="UTF-8") as f:
                f.write(json.dumps(obj=json_data, indent=4, sort_keys=True))
            # check response for error

            if "error" in json_data:
                logger.error(
                    "Error: " + json_data["error"] + " - " + json_data["message"]
                )
                sys.exit()
            # print number of packages found
            report_name = self.report_name()
            # if report_name == "identity":
            #     logging.info(msg="Start download of dataMart identity")
            # else:
            #     logging.info(msg="Start download of dataMart " + str(report_name) +
            #                  " - downloading " + str(get_number_of_packages(json_data["items"])) +
            #                  " package(s)")
            # Start looping through packages and items from JSON response
            package_number = 0

            for item in json_data["items"]:
                schema_url = item["schemaUrl"]
                prefix = ""
                # range_start_dt = ""
                # range_end_dt = ""
                # only for detail and dbtReport data mart display the ranges

                if report_name == "detail" or report_name == "dbtReport":
                    range_start_dt = item["dataRangeStartTimeStamp"]
                    range_start = range_start_dt.replace(":", "-").replace(".000Z", "")
                    # range_end_dt = item["dataRangeEndTimeStamp"]
                    # range_end = range_end_dt.replace(":", "-").replace(".999Z", "")
                    prefix = range_start + "_"
                    package_number = package_number + 1
                    # str_package_number = str(package_number)
                    # add a zero in front of package number if number is lower 10
                    # if package_number < 10:
                    #     str_package_number = "0" + str_package_number
                    # logging.info(msg="********** Tables of package " + str_package_number +
                    #              " - start: " + str(range_start) + " **********")
                    # print("\n  Tables of package " + str_package_number + " - start: " +
                    #       str(range_start), sep="", end="", flush=True)

                for entity in json_data["items"][package_number - 1]["entities"]:
                    create_data = CreateData.CreateData.get_instance()
                    create_data.entity(entity)
                    create_data.schema_url(schema_url)
                    create_data.create_single_table_files()

                    download_entity = DownloadEntity.DownloadEntity.get_instance()
                    download_entity.report_name(report_name)
                    download_entity.entity(entity)
                    download_entity.schema_url(schema_url)
                    download_entity.prefix(prefix)
                    download_entity.download_entity()
                clean_data = CleanData.CleanData.get_instance()
                clean_data.report_date(report_date.replace("-", "_").replace(":", "_"))
                clean_data.run()
            build_data = BuildEmailData.BuildEmailData.get_instance()
            build_data.build_email_list()
            if flag_test_report is False:
                connection = Connection.Connection.get_instance()
                result = connection.post_file_transfer_location()
                logger.info(msg=result)
            # track end time
            run_end = time.time()
            run_duration = round((run_end - run_start), 2)
            logger.info(msg=run_duration)
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None
        finally:
            return


if __name__ == "__main__":
    DownloadDiscover.__init__(DownloadDiscover())
