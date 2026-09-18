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
import sys
from pathlib import Path

import ftfy

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class CleanData:
    __instance = None

    @staticmethod
    def get_instance():
        if CleanData.__instance is None:
            CleanData()
        return CleanData.__instance

    def __init__(self, **kwargs):
        self._log_file = Path(
            "{0}{1}{2}".format(pkg_path, "/logs/", "standard_clean_data.log")
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        if CleanData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CleanData.__instance = self

        if "report_date" in kwargs:
            self._report_date = kwargs["report_date"]

    def report_date(self, value=None):
        if value:
            self._report_date = value
        try:
            return self._report_date
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

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
                    lineterminator="\r\n",
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
                            ftfy.fix_text(
                                i,
                                "*",
                                fix_entities="auto",
                                remove_terminal_escapes=True,
                                fix_encoding=True,
                                fix_latin_ligatures=True,
                                fix_character_width=True,
                                uncurl_quotes=True,
                                fix_line_breaks=True,
                                fix_surrogates=True,
                                remove_control_chars=True,
                                remove_bom=True,
                                normalization="NFC",
                                max_decode_length=1000000,
                            )
                            row[i] = ftfy.fix_text(
                                row[i],
                                fix_entities=True,
                                fix_encoding=True,
                                uncurl_quotes=True,
                                fix_latin_ligatures=True,
                                fix_character_width=True,
                                fix_surrogates=True,
                                remove_control_chars=True,
                                normalization="NKFC",
                            )
                            row[i] = ftfy.fix_text(row[i])
                        csv_writer.writerow(row)
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def clean_foreign_data(self):
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
                    lineterminator="\r\n",
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
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return

    def run(self):
        try:
            self.clean_control_data(self)
            self.clean_foreign_data()
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return


if __name__ == "__main__":
    CleanData.__init__(CleanData())
