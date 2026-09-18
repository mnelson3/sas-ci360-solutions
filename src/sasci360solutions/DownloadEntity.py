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
import gzip
from pathlib import Path

import requests
from connection import root_path
from log import Log

from standard import CreateData, Standard

_log_file_ = Path(root_path + Standard.gDirLog + "standard-download_entity.log")
_log_ = Log.Log.get_instance()
_log_.log_file(_log_file_)
logger = _log_.logging()


class DownloadEntity:
    __instance = None

    @staticmethod
    def get_instance():
        if DownloadEntity.__instance is None:
            DownloadEntity()
        return DownloadEntity.__instance

    def __init__(self, **kwargs):
        if DownloadEntity.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DownloadEntity.__instance = self

        standard = Standard.Standard.get_instance()

        self._delimiter = standard.delimiter()
        self._flag_append = standard.flag_append()
        self._flag_csv = standard.flag_csv()

        if "entity" in kwargs:
            self._entity = kwargs["entity"]
        if "prefix" in kwargs:
            self._prefix = kwargs["prefix"]
        if "schema_url" in kwargs:
            self._schema_url = kwargs["schema_url"]

    def entity(self, value=None):
        if value:
            self._entity = value
        try:
            return self._entity
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def prefix(self, value=None):
        if value:
            self._prefix = value
        try:
            return self._prefix
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def schema_url(self, value=None):
        if value:
            self._schema_url = value
        try:
            return self._schema_url
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None

    def download_entity(self, response=None):
        try:
            soh_delimiter = Standard.gSohDelimiter

            delimiter = self._delimiter
            flag_append = self._flag_append
            flag_csv = self._flag_csv
            entity = self.entity()
            prefix = self.prefix()
            schema_url = self.schema_url()

            name = entity["entityName"]

            create_data = CreateData.CreateData.get_instance()
            header = create_data.get_schema(
                entity=name, schema_url=schema_url, delimiter=delimiter
            )
            zipped_file = Path(root_path + Standard.gDsDscExtr + prefix + name + ".gz")
            unzipped_file = Path(
                root_path + Standard.gDsDscZip + prefix + name + ".soh"
            )
            csv_file = Path(root_path + Standard.gDsDscCsv + prefix + name + ".csv")
            # sql_file = Path(os.path.dirname(os.getcwd()) + Common.gDsDscSql + prefix +
            #                 "create_tables_" + report_name + ".sql")
            table_file = Path(root_path + Standard.gDsDscCsv + name + ".csv")

            i = 0
            for dataUrlDetail in entity["dataUrlDetails"]:
                i = i + 1
                url = dataUrlDetail["url"]
                response = requests.get(url=url, stream=True)
                response.encoding = "UTF-8"
                with open(file=zipped_file, mode="wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                        f.flush()
                f.close()
                response.close()

            with gzip.open(filename=zipped_file, mode="rb") as zipped, open(
                file=unzipped_file, mode="wb"
            ) as unzipped:
                unzipped_content = zipped.read()
                unzipped.write(unzipped_content)

            if (flag_csv is True) and (flag_append is False):
                create_data.in_file(unzipped_file)
                create_data.out_file(csv_file)
                create_data.in_delimiter(soh_delimiter)
                create_data.out_delimiter(delimiter)
                create_data.header(header)
                create_data.create_csv()
            elif (flag_csv is True) and (flag_append is True):
                create_data.in_file(unzipped_file)
                create_data.out_file(table_file)
                create_data.in_delimiter(soh_delimiter)
                create_data.out_delimiter(delimiter)
                create_data.append_csv()
        except Exception as e:
            logger.exception("Exception occurred: " + str(e))
            return None
        finally:
            return response


if __name__ == "__main__":
    DownloadEntity.__init__(DownloadEntity())
