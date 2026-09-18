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
import json
import logging
import os
import sys
from pathlib import Path

import requests

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class CreateData:
    __instance = None

    @staticmethod
    def get_instance():
        if CreateData.__instance is None:
            CreateData()
        return CreateData.__instance

    def __init__(self, **kwargs):
        self._log_file = Path(
            "{0}{1}{2}".format(pkg_path, "/logs/", "standard_create_data.log")
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        if CreateData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateData.__instance = self

        standard = Standard.Standard.get_instance()

        self._flag_csv_header = standard.flag_csv_header()
        self._delimiter = standard.delimiter()

        if "entity" in kwargs:
            self.entity = kwargs["entity"]
        if "header" in kwargs:
            self.header = kwargs["header"]
        if "in_delimiter" in kwargs:
            self.in_delimiter = kwargs["in_delimiter"]
        if "in_file" in kwargs:
            self.in_file = kwargs["in_file"]
        if "out_delimiter" in kwargs:
            self.out_delimiter = kwargs["out_delimiter"]
        if "out_file" in kwargs:
            self.out_file = kwargs["out_file"]
        if "report_date" in kwargs:
            self.report_date = kwargs["report_date"]
        if "schema_url" in kwargs:
            self.schema_url = kwargs["schema_url"]

    def create_csv(self):
        try:
            in_delimiter = Standard.gSohDelimiter
            flag_csv_header = self._flag_csv_header
            in_file = self.in_file()
            header = self.header()
            out_delimiter = self._delimiter
            out_file = self.out_file()
            with open(file=str(in_file), mode="r", encoding="UTF-8") as in_f, open(
                file=str(out_file), mode="a", encoding="UTF-8"
            ) as out_f:
                if flag_csv_header is True:
                    out_f.write(str(header) + "\n")
                rows = 0
                for line in in_f:
                    rows = rows + 1
                    try:
                        line = line.replace("|", "-").replace(
                            str(in_delimiter), str(out_delimiter)
                        )
                        out_f.write(line + "\n")
                    except (AttributeError, Exception) as e:
                        self.logger.exception("Exception occurred: {}".format(str(e)))
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def append_csv(self):
        try:
            in_delimiter = Standard.gSohDelimiter
            in_file = self.in_file()
            out_delimiter = self._delimiter
            out_file = self.out_file()
            with open(file=str(in_file), mode="r", encoding="UTF-8") as in_f, open(
                file=str(out_file), mode="a", encoding="UTF-8"
            ) as out_f:
                rows = 0
                for line in in_f:
                    rows = rows + 1
                    try:
                        line = line.replace("|", "-").replace(
                            str(in_delimiter), str(out_delimiter)
                        )
                        out_f.write(line + "\n")
                    except Exception as e:
                        self.logger.exception("Exception occurred: {}".format(str(e)))
                        return None
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def create_single_table_files(self):
        try:
            delimiter = self._delimiter
            entity = self.entity()
            schema_url = self.schema_url()
            name = entity["entityName"]
            table_file = Path(root_path + Standard.gDsDscCsv + name + ".csv")
            if not os.path.exists(table_file):
                header = self.get_schema(
                    entity=name, schema_url=schema_url, delimiter=delimiter
                )
                with open(file=table_file, mode="w", encoding="UTF-8") as f:
                    f.write(header + "\n")
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def get_schema(self, entity, schema_url, delimiter):
        column_header = ""
        sql_column = ""
        sql_insert_column = ""
        try:
            table_name = entity
            url = schema_url
            delimiter = delimiter
            response = requests.get(url=url).text.encode(
                encoding="UTF-8", errors="replace"
            )
            json_meta = json.loads(response)
            sql_table = "create table " + table_name + "("
            sql_insert = "insert into " + table_name + " values ("
            for item in json_meta:
                meta_table = item["table_name"]
                if table_name.lower() == meta_table.lower():
                    column = str(item["column_name"])
                    column_type = str(item["column_type"])
                    sql_column = sql_column + "\n  " + column + " " + column_type + ", "
                    sql_insert_column = sql_insert_column + "%s,"
                    column_header = column_header + column + delimiter
            Standard.gSql += sql_table + sql_column[:-2] + ");\n\n"
            Standard.gSqlInsert = sql_insert + sql_insert_column[:-1] + ")"
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            # remove last delimiter and return line
            return column_header[: -len(delimiter)]


if __name__ == "__main__":
    CreateData.__init__(CreateData())
