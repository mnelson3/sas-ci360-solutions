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
