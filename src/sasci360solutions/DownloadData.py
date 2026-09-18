# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import gzip
import logging
from pathlib import Path

import requests
from discover import CreateData

from standard import Standard, root_path


class DownloadData:

    def __init__(self, **kwargs):
        log_file = Path(root_path + Standard.gDirLog + "discover-downloaddata.log")
        logger = logging.getLogger()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        standard = Standard.Standard()

        self._delimiter = standard.delimiter()
        self._flag_append = standard.flag_append()
        self._flag_csv = standard.flag_csv()

        if "entity" in kwargs:
            self._entity = kwargs["entity"]
        if "header" in kwargs:
            self._header = kwargs["header"]
        if "in_delimiter" in kwargs:
            self._in_delimiter = kwargs["in_delimiter"]
        if "in_file" in kwargs:
            self._in_file = kwargs["in_file"]
        if "out_delimiter" in kwargs:
            self._out_delimiter = kwargs["out_delimiter"]
        if "out_file" in kwargs:
            self._out_file = kwargs["out_file"]
        if "prefix" in kwargs:
            self._prefix = kwargs["prefix"]
        if "report_date" in kwargs:
            self._report_date = kwargs["report_date"]
        if "report_name" in kwargs:
            self._report_name = kwargs["report_name"]
        if "schema_url" in kwargs:
            self._schema_url = kwargs["schema_url"]

    def delimiter(self, value=None):
        if value:
            self._delimiter = value
        try:
            return self._delimiter
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def flag_append(self, value=None):
        if value:
            self._flag_append = value
        try:
            return bool(self._flag_append)
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def flag_csv(self, value=None):
        if value:
            self._flag_csv = value
        try:
            return bool(self._flag_csv)
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def entity(self, value=None):
        if value:
            self._entity = value
        try:
            return self._entity
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def header(self, value=None):
        if value:
            self._header = value
        try:
            return self._header
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def in_delimiter(self, value=None):
        if value:
            self._in_delimiter = value
        try:
            return self._in_delimiter
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def in_file(self, value=None):
        if value:
            self._in_file = value
        try:
            return self._in_file
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def out_delimiter(self, value=None):
        if value:
            self._out_delimiter = value
        try:
            return self._out_delimiter
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def out_file(self, value=None):
        if value:
            self._out_file = value
        try:
            return self._out_file
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def prefix(self, value=None):
        if value:
            self._prefix = value
        try:
            return self._prefix
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def report_date(self, value=None):
        if value:
            self._report_date = value
        try:
            return self._report_date
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def report_name(self, value=None):
        if value:
            self._report_name = value
        try:
            return self._report_name
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def schema_url(self, value=None):
        if value:
            self._schema_url = value
        try:
            return self._schema_url
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def download_entity(self):
        try:
            soh_delimiter = Standard.gSohDelimiter

            delimiter = self.delimiter()
            flag_append = self.flag_append()
            flag_csv = self.flag_csv()
            entity = self.entity()
            schema_url = self.schema_url()
            prefix = self.prefix()

            name = entity["entityName"]

            create_data = CreateData.CreateData()
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
            logging.exception("Exception occurred: " + str(e))
            return None
        finally:
            return


if __name__ == "__main__":
    DownloadData.__init__(DownloadData())
