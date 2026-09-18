# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
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

        standard = Standard.get_instance()

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
