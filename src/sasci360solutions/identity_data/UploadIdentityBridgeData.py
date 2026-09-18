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

from sasci360apicore import connection, encryption, reporter

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class UploadIdentityBridgeData:

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

        self.connection = connection.Connection()
        self.reporter = reporter.Reporter(root=root_path)

        self.standard = Standard(mode=self.mode)
        self.security = encryption.Encryption(
            algorithm=self.standard.algorithm, encoding=self.standard.encoding
        )
        self._export_file = self.standard.export_file
        self.export_path = self.standard.export_path
        self._export_post_path = self.standard.export_post_path
        self.external_gateway_path = self.standard.external_gateway_path
        self.secret_key = self.standard.secret_key
        self.tenant_id = self.standard.tenant_id

        self.gDirDataResponseFileTransferLocationPost = (
            self.standard.gDirDataResponseFileTransferLocationPost
        )
        self.file_transfer_location_path = self.standard.file_transfer_location_path

    def run(self, result=None, **kwargs):
        try:
            time_stamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
            time_stamp_ = time_stamp.replace(":", "")

            if self.mode is not None:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, self.mode
                )
            else:
                folder = "{0}{1}/".format(
                    self.gDirDataResponseFileTransferLocationPost, "development"
                )

            export_folder = self.export_path
            external_gateway_path = self.external_gateway_path
            file_transfer_location_path = self.file_transfer_location_path

            secret_key = self.secret_key
            tenant_id = self.tenant_id
            token = self.security.generate_jwt(
                secret_key=secret_key, tenant_id=tenant_id
            )

            action = "POST"
            data = None
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {0}".format(token),
            }
            params = None
            url = "https://{0}{1}".format(
                external_gateway_path, file_transfer_location_path
            )
            result = self.connection.connect(
                action=action, data=data, headers=headers, params=params, url=url
            )
            self.reporter.save(
                folder=folder,
                name="file_transfer_location_post_{}".format(time_stamp_),
                data=result,
            )

            __signed_url = None
            if result is not None:
                __signed_url = result["signedURL"]
            temporary_url = __signed_url

            if "file_name" in kwargs:
                file_name = kwargs["file_name"]
                csv_file = Path("{0}".format(file_name))
            else:
                file_post_path = self._export_post_path
                file_export_path = Path("{0}{1}".format(root_path, self.export_path))
                file_export = self._export_file
                file_export_timestamp = "{0}_{1}{2}".format(
                    file_export[:-4], time_stamp_, ".CSV"
                )
                shutil.copy(
                    Path("{0}/{1}".format(file_post_path, file_export)),
                    Path("{0}/{1}".format(file_export_path, file_export_timestamp)),
                )
                file_name = "{0}_{1}".format(file_export[:-4], time_stamp_)
                csv_file = Path(
                    "{0}{1}{2}{3}".format(root_path, export_folder, file_name, ".CSV")
                )

            result = None
            action = "PUT"
            data = csv_file
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            params = None
            url = temporary_url
            result = self.connection.connect(
                action=action, data=data, headers=headers, params=params, url=url
            )
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return result


if __name__ == "__main__":
    UploadIdentityBridgeData.__init__(UploadIdentityBridgeData())
