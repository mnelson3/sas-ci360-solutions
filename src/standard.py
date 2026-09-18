# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import configparser
import os
from configparser import ConfigParser
from pathlib import Path

# Global root_path variable
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Standard:
    """Standard configuration class providing constants and settings.

    Reads from config/config.ini (see config/config.ini.example), with
    dev/test/production variants for values that need to differ by
    environment. Pass mode="development"|"test"|"production" to select
    one; omit it to get the configured default.
    """

    # Directory path constants
    gDirLog = "/logs/"
    gDsDscCsv = "/data/csv/"
    gDsDscFix = "/data/fix/"
    gDsDscClean = "/data/clean/"
    gDsDscExport = "/data/export/"
    gDsDscConfig = "/config/"
    gDirDataResponseTablesGet = "/data/response/tables/"
    gDirDataResponseFileTransferLocationPost = "/data/response/file_transfer_location_post/"
    gDirDataResponseImportRequestJobsGet = "/data/response/import_request_jobs_get/"

    # Singleton instance
    _instance = None

    def __init__(self, **kwargs):
        """Initialize Standard configuration."""
        self.__mode = kwargs.get("mode")

        config_parser = ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config_file = Path("{0}{1}{2}".format(root_path, "/config/", "config.ini"))
        config_parser.read(config_file)

        # EMAIL
        self.email_msg_status_from = config_parser.get(
            "EMAIL", "email_msg_status_from", fallback="noreply@example.com"
        )
        self.email_msg_status_to = config_parser.get(
            "EMAIL", "email_msg_status_to", fallback="admin@example.com"
        )
        self._email_msg_support_from = config_parser.get(
            "EMAIL", "email_msg_support_from", fallback="support@nelsongrey.com"
        )
        self._email_msg_support_from_arr = config_parser.get(
            "EMAIL", "email_msg_support_from_arr", fallback=""
        )
        self._email_msg_support_to = config_parser.get(
            "EMAIL", "email_msg_support_to", fallback="support@nelsongrey.com"
        )
        self._email_msg_support_to_arr = config_parser.get(
            "EMAIL", "email_msg_support_to_arr", fallback=""
        )
        self._email_msg_support_cc = config_parser.get(
            "EMAIL", "email_msg_support_cc", fallback="support@nelsongrey.com"
        )
        self._email_msg_support_cc_arr = config_parser.get(
            "EMAIL", "email_msg_support_cc_arr", fallback=""
        )
        self.email_server = config_parser.get(
            "EMAIL", "email_server", fallback="smtp.example.com"
        )
        self.email_server_login = config_parser.get(
            "EMAIL", "email_server_login", fallback="automation@example.com"
        )
        self.email_server_password = config_parser.get(
            "EMAIL", "email_server_password", fallback="changeme"
        )
        self.email_server_port = config_parser.get(
            "EMAIL", "email_server_port", fallback="587"
        )

        # FILES
        self._export_file = config_parser.get("FILES", "export_file", fallback="export.csv")
        self._export_file_arr = config_parser.get("FILES", "export_file_arr", fallback="")
        self._export_change_file = config_parser.get(
            "FILES", "export_change_file", fallback="export_change.csv"
        )
        self._export_change_file_arr = config_parser.get(
            "FILES", "export_change_file_arr", fallback=""
        )

        # IDENTITIES
        self.identity_bridge_table_id = config_parser.get(
            "IDENTITIES", "identity_bridge_table_id", fallback="changeme"
        )
        self._secret_key = config_parser.get("IDENTITIES", "secret_key", fallback="changeme")
        self._secret_key_arr = config_parser.get("IDENTITIES", "secret_key_arr", fallback="")
        self._tenant_id = config_parser.get("IDENTITIES", "tenant_id", fallback="changeme")
        self._tenant_id_arr = config_parser.get("IDENTITIES", "tenant_id_arr", fallback="")

        # PATHS
        self._export_path = config_parser.get("PATHS", "export_path", fallback="/data/export/")
        self._export_path_arr = config_parser.get("PATHS", "export_path_arr", fallback="")
        self._export_post_path = config_parser.get(
            "PATHS", "export_post_path", fallback="changeme"
        )
        self._export_post_path_arr = config_parser.get(
            "PATHS", "export_post_path_arr", fallback=""
        )
        self._external_gateway_path = config_parser.get(
            "PATHS", "external_gateway_path", fallback="extapigwservice-training.ci360.sas.com"
        )
        self._external_gateway_path_arr = config_parser.get(
            "PATHS", "external_gateway_path_arr", fallback=""
        )
        self.file_transfer_location_path = config_parser.get(
            "PATHS", "file_transfer_location_path", fallback="/marketingData/fileTransferLocation"
        )
        self.import_request_jobs_path = config_parser.get(
            "PATHS", "import_request_jobs_path", fallback="/marketingData/importRequestJobs"
        )
        self.reports_path = config_parser.get("PATHS", "reports_path", fallback="/reports/")

        # SETTINGS
        self.algorithm = config_parser.get("SETTINGS", "algorithm", fallback="HS256")
        self.encoding = config_parser.get("SETTINGS", "encoding", fallback="UTF-8")
        self._tenant_environment = config_parser.get(
            "SETTINGS", "tenant_environment", fallback="test"
        )
        self._tenant_environment_arr = config_parser.get(
            "SETTINGS", "tenant_environment_arr", fallback=""
        )
        self._tenant_name = config_parser.get(
            "SETTINGS", "tenant_name", fallback="Example Tenant"
        )
        self._tenant_name_arr = config_parser.get("SETTINGS", "tenant_name_arr", fallback="")
        self._tenant_number = config_parser.get("SETTINGS", "tenant_number", fallback="000000")
        self._tenant_number_arr = config_parser.get("SETTINGS", "tenant_number_arr", fallback="")
        self._tenant_product = config_parser.get(
            "SETTINGS", "tenant_product", fallback="SAS Customer Intelligence 360"
        )
        self._tenant_product_arr = config_parser.get("SETTINGS", "tenant_product_arr", fallback="")
        self._tenant_url = config_parser.get(
            "SETTINGS",
            "tenant_url",
            fallback="https://platform-training.ci360.sas.com/SASCustomerIntelligenceHome/",
        )
        self._tenant_url_arr = config_parser.get("SETTINGS", "tenant_url_arr", fallback="")

        # Other settings
        self._delimiter = ","
        self._flag_test_report = True
        self._suppression_email_domain_list = []
        self._suppression_form_name_list = []

    @classmethod
    def get_instance(cls):
        """Get singleton instance of Standard."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _by_mode(self, arr_value, bare_value):
        """Select dev/test/production out of a comma-separated arr value."""
        if not arr_value:
            return bare_value
        parts = str(arr_value).split(",")
        index = {"development": 0, "test": 1, "production": 2}.get(self.__mode)
        if index is None or index >= len(parts):
            return bare_value
        return parts[index]

    def delimiter(self):
        """Get CSV delimiter."""
        return self._delimiter

    def flag_test_report(self):
        """Get test report flag."""
        return self._flag_test_report

    def suppression_email_domain_list(self):
        """Get suppression email domain list."""
        return self._suppression_email_domain_list

    def suppression_form_name_list(self):
        """Get suppression form name list."""
        return self._suppression_form_name_list

    def tables_path(self):
        """Get tables API path."""
        return "/marketingData/tables"

    @property
    def email_msg_support_from(self):
        return self._by_mode(self._email_msg_support_from_arr, self._email_msg_support_from)

    @property
    def email_msg_support_from_arr(self):
        return self._by_mode(self._email_msg_support_from_arr, self._email_msg_support_from_arr)

    @property
    def email_msg_support_to(self):
        return self._by_mode(self._email_msg_support_to_arr, self._email_msg_support_to)

    @property
    def email_msg_support_to_arr(self):
        return self._by_mode(self._email_msg_support_to_arr, self._email_msg_support_to_arr)

    @property
    def email_msg_support_cc(self):
        return self._by_mode(self._email_msg_support_cc_arr, self._email_msg_support_cc)

    @property
    def email_msg_support_cc_arr(self):
        return self._by_mode(self._email_msg_support_cc_arr, self._email_msg_support_cc_arr)

    @property
    def export_file(self):
        return self._by_mode(self._export_file_arr, self._export_file)

    @property
    def export_file_arr(self):
        return self._by_mode(self._export_file_arr, self._export_file_arr)

    @property
    def export_change_file(self):
        return self._by_mode(self._export_change_file_arr, self._export_change_file)

    @property
    def export_change_file_arr(self):
        return self._by_mode(self._export_change_file_arr, self._export_change_file_arr)

    @property
    def secret_key(self):
        return self._by_mode(self._secret_key_arr, self._secret_key)

    @property
    def secret_key_arr(self):
        return self._by_mode(self._secret_key_arr, self._secret_key_arr)

    @property
    def tenant_id(self):
        return self._by_mode(self._tenant_id_arr, self._tenant_id)

    @property
    def tenant_id_arr(self):
        return self._by_mode(self._tenant_id_arr, self._tenant_id_arr)

    @property
    def export_path(self):
        return self._by_mode(self._export_path_arr, self._export_path)

    @property
    def export_path_arr(self):
        return self._by_mode(self._export_path_arr, self._export_path_arr)

    @property
    def export_post_path(self):
        return self._by_mode(self._export_post_path_arr, self._export_post_path)

    @property
    def export_post_path_arr(self):
        return self._by_mode(self._export_post_path_arr, self._export_post_path_arr)

    @property
    def external_gateway_path(self):
        return self._by_mode(self._external_gateway_path_arr, self._external_gateway_path)

    @property
    def external_gateway_path_arr(self):
        return self._by_mode(self._external_gateway_path_arr, self._external_gateway_path_arr)

    @property
    def tenant_environment(self):
        return self._by_mode(self._tenant_environment_arr, self._tenant_environment)

    @property
    def tenant_environment_arr(self):
        return self._by_mode(self._tenant_environment_arr, self._tenant_environment_arr)

    @property
    def tenant_name(self):
        return self._by_mode(self._tenant_name_arr, self._tenant_name)

    @property
    def tenant_name_arr(self):
        return self._by_mode(self._tenant_name_arr, self._tenant_name_arr)

    @property
    def tenant_number(self):
        return self._by_mode(self._tenant_number_arr, self._tenant_number)

    @property
    def tenant_number_arr(self):
        return self._by_mode(self._tenant_number_arr, self._tenant_number_arr)

    @property
    def tenant_product(self):
        return self._by_mode(self._tenant_product_arr, self._tenant_product)

    @property
    def tenant_product_arr(self):
        return self._by_mode(self._tenant_product_arr, self._tenant_product_arr)

    @property
    def tenant_url(self):
        return self._by_mode(self._tenant_url_arr, self._tenant_url)

    @property
    def tenant_url_arr(self):
        return self._by_mode(self._tenant_url_arr, self._tenant_url_arr)


# Export classes and variables
__all__ = ["Standard", "root_path"]
