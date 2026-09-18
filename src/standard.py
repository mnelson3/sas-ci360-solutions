# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import os


class Standard:
    """Standard configuration class providing constants and settings."""

    # Directory path constants
    gDirLog = "/logs/"
    gDsDscCsv = "/data/csv/"
    gDsDscFix = "/data/fix/"
    gDsDscClean = "/data/clean/"
    gDsDscExport = "/data/export/"
    gDsDscConfig = "/config/"
    gDirDataResponseTablesGet = "/data/response/tables/"

    # Singleton instance
    _instance = None

    def __init__(self):
        """Initialize Standard configuration."""
        # Email settings
        self.email_msg_status_from = "noreply@sas.com"
        self.email_msg_status_to = "admin@sas.com"
        self.email_msg_support_from = "support@nelsongrey.com"
        self.email_msg_support_to = "support@nelsongrey.com"
        self.reports_path = "/reports/"

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


# Global root_path variable
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Export classes and variables
__all__ = ["Standard", "root_path"]
