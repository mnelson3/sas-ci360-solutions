# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import codecs
import csv
import logging
import os
from pathlib import Path

import ftfy

from standard import Standard, root_path


class CleanData:

    def __init__(self, **kwargs):
        log_file = Path(root_path + Standard.gDirLog + "discover-cleandata.log")
        logger = logging.getLogger()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        if "report_date" in kwargs:
            self._report_date = kwargs["report_date"]

    def report_date(self, value=None):
        if value:
            self._report_date = value
        try:
            return self._report_date
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def clean_control_data(self):
        try:
            report_date = self.report_date()
            path = Path(root_path + Standard.gDsDscCsv)
            for filename in os.listdir(path=path):
                file_name = os.path.splitext(filename)[0]
                file_path = path.joinpath(filename)
                table_name = str(file_name) + "_" + str(report_date) + ".csv"
                out_path = Path(root_path + Standard.gDsDscFix + table_name)
                csv.register_dialect(
                    "sas",
                    delimiter="|",
                    lineterminator="\n",
                    escapechar="\\",
                    quoting=csv.QUOTE_NONE,
                )
                with open(
                    file=file_path,
                    mode="r",
                    newline="",
                    encoding="UTF-8",
                    errors="replace",
                ) as in_file, open(
                    file=out_path,
                    mode="w",
                    newline="",
                    encoding="UTF-8",
                    errors="replace",
                ) as out_file:
                    csv_reader = csv.reader(in_file, dialect="sas")
                    csv_writer = csv.writer(out_file, dialect="sas")
                    for row in csv_reader:
                        for i in range(len(row)):
                            row[i] = ftfy.fix_text(
                                row[i],
                                fix_encoding=True,
                                uncurl_quotes=True,
                                fix_latin_ligatures=True,
                                fix_character_width=True,
                                fix_line_breaks=True,
                                fix_surrogates=True,
                                remove_control_chars=True,
                                normalization="NFKC",
                            )
                        csv_writer.writerow(row)
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None
        finally:
            return

    @staticmethod
    def clean_foreign_data():
        try:
            path = Path(root_path + Standard.gDsDscFix)
            for filename in os.listdir(path=path):
                file_name = os.path.splitext(filename)[0]
                file_path = path.joinpath(filename)
                table_name = str(file_name) + ".csv"
                out_path = Path(root_path + Standard.gDsDscClean + table_name)
                csv.register_dialect(
                    "sas",
                    delimiter="|",
                    lineterminator="\n",
                    escapechar="\\",
                    quoting=csv.QUOTE_NONE,
                )
                with codecs.open(
                    filename=file_path, mode="r", encoding="UTF-8", errors="replace"
                ) as in_file, codecs.open(
                    filename=out_path, mode="w", encoding="UTF-8", errors="replace"
                ) as out_file:
                    csv_reader = csv.reader(in_file, dialect="sas")
                    csv_writer = csv.writer(out_file, dialect="sas")
                    for row in csv_reader:
                        for i in range(len(row)):
                            for c in range(len(row[i])):
                                try:
                                    if ord(row[i][c]) > 256:
                                        row[i] = str(row[i]).replace(row[i][c], "?")
                                except (
                                    IndexError,
                                    UnicodeError,
                                    UnicodeEncodeError,
                                    UnicodeDecodeError,
                                ):
                                    row[i] = str(row[i]).replace(row[i][c], "?")
                        csv_writer.writerow(row)
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None
        finally:
            return

    def run(self):
        try:
            self.clean_control_data()
            self.clean_foreign_data()
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None
        finally:
            return


if __name__ == "__main__":
    CleanData.__init__(CleanData())
