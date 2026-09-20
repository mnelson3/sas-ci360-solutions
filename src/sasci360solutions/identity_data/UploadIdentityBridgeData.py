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
import shutil
import sys
from datetime import datetime
from pathlib import Path

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


class UploadIdentityBridgeData:
    """Uploads a local identity-bridge CSV to CI360 via the file-transfer-location
    signed-URL flow, using the sol-data client (sasci360soldata)."""

    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode")

        self._log_file = Path(
            "{0}{1}{2}".format(
                pkg_path, "/logs/", "custom_upload_identity_bridge_data.log"
            )
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        self.root_path = kwargs.get("root_path", root_path)
        self.standard = kwargs.get("standard") or Standard(mode=self.mode)

        self.client = kwargs.get("client") or CI360DataBase(
            CI360DataConfig(
                algorithm=self.standard.algorithm,
                encoding=self.standard.encoding,
                host="https://{0}".format(self.standard.external_gateway_path),
                secret_key=self.standard.secret_key,
                tenant_id=self.standard.tenant_id,
            )
        )

        self.reporter = kwargs.get("reporter") or reporter.Reporter(root=self.root_path)

        self._export_file = self.standard.export_file
        self.export_path = self.standard.export_path
        self._export_post_path = self.standard.export_post_path
        self.gDirDataResponseFileTransferLocationPost = (
            self.standard.gDirDataResponseFileTransferLocationPost
        )

    def run(self, **kwargs):
        """
        Upload an identity-bridge CSV to CI360.

        :keyword file_name: path to a specific CSV to upload; if omitted,
            the configured default export file is used.
        :return: True if the upload succeeded, False otherwise.
        :rtype: bool
        """
        result = False
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            time_stamp_ = time_stamp.replace(":", "")

            if "file_name" in kwargs:
                csv_file = Path("{0}".format(kwargs["file_name"]))
            else:
                file_post_path = self._export_post_path
                file_export_path = Path(
                    "{0}{1}".format(self.root_path, self.export_path)
                )
                file_export = self._export_file
                file_export_timestamp = "{0}_{1}{2}".format(
                    file_export[:-4], time_stamp_, ".CSV"
                )
                shutil.copy(
                    Path("{0}/{1}".format(file_post_path, file_export)),
                    Path("{0}/{1}".format(file_export_path, file_export_timestamp)),
                )
                csv_file = Path(
                    "{0}{1}{2}".format(file_export_path, "/", file_export_timestamp)
                )

            transfer_location = self.client.create_file_transfer_location()

            if self.mode is not None:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, self.mode
                )
            else:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, "development"
                )
            self.reporter.save(
                folder=folder,
                name="file_transfer_location_post_{}".format(time_stamp_),
                data=transfer_location,
            )

            signed_url = (
                transfer_location.get("signedURL") if transfer_location else None
            )
            if not signed_url:
                self.logger.error(
                    "No signedURL returned by create_file_transfer_location"
                )
                return False

            result = self.client.upload_to_signed_url(signed_url, str(csv_file))
        except (TypeError, KeyError, OSError, CI360DataError) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
            result = False
        return result


if __name__ == "__main__":
    UploadIdentityBridgeData.__init__(UploadIdentityBridgeData())
