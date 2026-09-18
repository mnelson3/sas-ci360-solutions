# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from sasci360apicore import connection, reporter

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class TableActions:
    __mode = None

    def __init__(self, **kwargs):
        self._log_file = Path(
            "{0}{1}{2}".format(pkg_path, "/logs/", "custom_tables_action.log")
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        if "mode" in kwargs:
            TableActions.__mode = kwargs["mode"]
        else:
            TableActions.__mode = None
        self.__mode = TableActions.__mode

        self._reporter = reporter.Reporter()
        self._standard = Standard.Standard()
        self._export_file = self._standard.export_file
        self._export_path = self._standard.export_path
        self._export_post_path = self._standard.export_post_path
        self._external_gateway_path = self._standard.external_gateway_path
        self._secret_key = self._standard.secret_key
        self._tenant_id = self._standard.tenant_id

        self._connection = connection.Connection()
        # self._security = Security.Security()
        self._gDirDataResponseFileTransferLocationPost = (
            self._standard.gDirDataResponseFileTransferLocationPost
        )
        self._file_transfer_location_path = self._standard.file_transfer_location_path

    def tables_get(self):
        time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        time_stamp_ = time_stamp.replace(":", "")

        folder = self._standard.gDirDataResponseTablesGet

        # secret_key = self._secret_key
        # tenant_id = self._tenant_id
        token = os.getenv("SAS_CI360_TOKEN", "")

        action = "GET"
        data = None
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(token),
        }
        params = None
        url = "https://{0}".format(self._standard.tables_path)
        result = self._connection.conn(
            action=action, data=data, headers=headers, params=params, url=url
        )
        self._reporter.store_response(
            folder=folder, name="table_get_{}".format(time_stamp_), data=result
        )

    def tables_by_id_get(self, **kwargs):
        time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")

        folder = self._standard.gDirDataResponseTablesGet

        # secret_key = self._secret_key
        # tenant_id = self._tenant_id
        token = os.getenv("SAS_CI360_TOKEN", "")

        if "table_id" in kwargs:
            table_id = kwargs["table_id"]
        # else:
        # table_id = self._standard.identity_bridge_table_id
        # assert table_id == self._standard.identity_bridge_table_id

        file_name = "table_get_{}".format(time_stamp)
        json_file = Path(
            "{0}{1}{2}{3}".format(
                root_path, self._standard.gDirDataResponseTablesGet, file_name, ".JSON"
            )
        )

        print("json_file : {}".format(json_file))
        with open(json_file, "r", encoding="utf-8") as outfile:
            result = json.load(outfile)
            __url = None
            if result is not None:
                for item in result["items"]:
                    if item["id"] == table_id:
                        for i in item["links"]:
                            if i["method"] == "GET":
                                __url = i["href"]
                                print("__url : {0}".format(__url))
            temporary_url = __url

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
            action=action, data=data, headers=headers, params=params, url=url
        )
        folder = self._standard.gDirDataResponseTablesGet
        self._reporter.store_response(
            folder=folder, name="{}".format(table_id), data=result
        )
        self._reporter.store_response(
            folder=folder, name="{}".format(table_id), data=result
        )


if __name__ == "__main__":
    TableActions.__init__(TableActions())
