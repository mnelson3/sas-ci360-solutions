# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from sasci360apicore import reporter
from sasci360soldata.base import CI360DataBase, CI360DataConfig, CI360DataError

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class TableActions:
    """Reads customer-table metadata from CI360's Marketing Data API via the
    sol-data client."""

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")

        self._log_file = Path(
            "{0}{1}{2}".format(pkg_path, "/logs/", "custom_tables_action.log")
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.root_path = kwargs.get("root_path", root_path)
        self.standard = kwargs.get("standard") or Standard(mode=self.mode)
        self.reporter = kwargs.get("reporter") or reporter.Reporter(root=self.root_path)

        self.client = kwargs.get("client") or CI360DataBase(
            CI360DataConfig(
                algorithm=self.standard.algorithm,
                encoding=self.standard.encoding,
                host="https://{0}".format(self.standard.external_gateway_path),
                secret_key=self.standard.secret_key,
                tenant_id=self.standard.tenant_id,
            )
        )

    def tables_get(self) -> Optional[dict]:
        """
        Fetch and persist a summary of all customer tables.

        :return: the parsed tables-summary response, or None on failure.
        :rtype: dict
        """
        try:
            time_stamp_ = datetime.now().strftime("%Y%m%d%H%M%S")
            tables = self.client.get_tables()
            self.reporter.save(
                folder=self.standard.gDirDataResponseTablesGet,
                name="table_get_{}".format(time_stamp_),
                data=tables,
            )
            return tables
        except (KeyError, OSError, CI360DataError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return None

    def tables_by_id_get(self, **kwargs) -> Optional[dict]:
        """
        Fetch and persist a single table's metadata by ID.

        :keyword table_id: required - the table's unique ID
        :return: the parsed table response, or None on failure.
        :rtype: dict
        """
        table_id = kwargs.get("table_id")
        if not table_id:
            raise ValueError("table_id is required")

        try:
            table = self.client.get_table(table_id)
            self.reporter.save(
                folder=self.standard.gDirDataResponseTablesGet,
                name="{}".format(table_id),
                data=table,
            )
            return table
        except (KeyError, OSError, CI360DataError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            return None


if __name__ == "__main__":
    TableActions.__init__(TableActions())
