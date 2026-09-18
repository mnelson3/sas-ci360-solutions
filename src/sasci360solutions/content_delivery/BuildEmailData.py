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

# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Business Source License 1.1 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas

from standard import Standard

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class BuildEmailData:
    # __mode = None
    __instance = None

    @staticmethod
    def get_instance():
        if BuildEmailData.__instance is None:
            BuildEmailData()
        return BuildEmailData.__instance

    def __init__(self, **kwargs):
        self._log_file = Path(
            "{0}{1}{2}".format(pkg_path, "/logs/", "custom_build_email_data.log")
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        if BuildEmailData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BuildEmailData.__instance = self

        self.standard = Standard.Standard()
        self.export_path = self._standard.export_path
        self.export_file = self._standard.export_file
        self.flag_test_export = self._standard.flag_test_export
        self.flag_test_report = self._standard.flag_test_report
        self.suppression_email_domain_list = (
            self._standard.suppression_email_domain_list()
        )
        self.suppression_form_name_list = self._standard.suppression_form_name_list()

    def build_email_list(self):
        try:
            flag_test_export = self.flag_test_export
            flag_test_report = self.flag_test_report

            if flag_test_export is True:
                customer_datamart = Path(
                    self.export_test_path + "identity_bridge_data.csv"
                )
            else:
                customer_datamart = Path(
                    self.export_prod_path + "identity_bridge_data.csv"
                )

            customer_datamart_dataframe = pandas.read_csv(
                filepath_or_buffer=customer_datamart,
                sep=",",
                delimiter=",",
                encoding="UTF-8",
            )
            suppression_email_domain_list = self.suppression_email_domain_list
            # suppression_form_name_list = self.suppression_form_name_list()

            today = pandas.to_datetime(datetime.now())
            current_hour_datetime = today.floor("H").to_pydatetime()
            suppression_hour = today + timedelta(hours=-1)
            suppression_hour_datetime = suppression_hour.floor("H").to_pydatetime()
            target_hour = today + timedelta(hours=-2)
            target_hour_datetime = target_hour.floor("H").to_pydatetime()
            path = Path(root_path + Standard.gDsDscClean)
            folder = (
                str(datetime.now())
                .replace(" ", "_")
                .replace(":", "_")
                .replace("-", "_")
                .replace(".", "_")
            )

            if flag_test_export is True and flag_test_report is True:
                path_out = Path(Standard.gCustomerDataMartProd + "/" + folder + "/")
                os.makedirs(path_out)
            elif flag_test_export is True and flag_test_report is False:
                path_out = Path(
                    root_path + Standard.gDsDscExport + Standard.gDsDscExportTestFile
                )
            else:
                path_out = Path(
                    root_path + Standard.gDsDscExport + Standard.gDsDscExportProdFile
                )

            page_details_dataframe = pandas.DataFrame()
            form_details_dataframe = pandas.DataFrame()

            for filename in os.listdir(path=path):
                if str(filename).startswith("PAGE_DETAILS") and not str(
                    filename
                ).startswith("PAGE_DETAILS_EXT"):
                    file_path = path.joinpath(filename)
                    page_details_dataframe = pandas.read_csv(
                        filepath_or_buffer=file_path,
                        sep="|",
                        delimiter="|",
                        encoding="UTF-8",
                    )
                if str(filename).startswith("FORM_DETAILS"):
                    file_path = path.joinpath(filename)
                    form_details_dataframe = pandas.read_csv(
                        filepath_or_buffer=file_path,
                        sep="|",
                        delimiter="|",
                        encoding="UTF-8",
                    )

            if flag_test_export is True and flag_test_report is True:
                page_details_dataframe.to_csv(
                    path_or_buf=path_out.joinpath("page_details_dataframe.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )
                form_details_dataframe.to_csv(
                    path_or_buf=path_out.joinpath("form_details_dataframe.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            target_page_details_dataframe = page_details_dataframe
            suppression_page_details_dataframe = page_details_dataframe
            target_form_details_dataframe = form_details_dataframe
            suppression_form_details_dataframe = form_details_dataframe

            target_page_details_df = target_page_details_dataframe[
                (
                    target_page_details_dataframe["detail_dttm_tz"]
                    > str(target_hour_datetime)
                )
                & (
                    target_page_details_dataframe["detail_dttm_tz"]
                    <= str(suppression_hour_datetime)
                )
                & (
                    target_page_details_dataframe["domain_nm"]
                    == "support.worldwildlife.org"
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                target_page_details_df.to_csv(
                    path_or_buf=path_out.joinpath("target_page_details_df.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            target_form_details_df = target_form_details_dataframe[
                (
                    target_form_details_dataframe.detail_id.isin(
                        target_page_details_df.detail_id
                    )
                )
                & (
                    target_form_details_dataframe.identity_id.isin(
                        target_page_details_df.identity_id
                    )
                )
                & (
                    target_form_details_dataframe["form_field_detail_dttm_tz"]
                    > str(target_hour_datetime)
                )
                & (
                    target_form_details_dataframe["form_field_detail_dttm_tz"]
                    <= str(suppression_hour_datetime)
                )
                & (
                    target_form_details_dataframe["attempt_status_cd"]
                    == "0_Not Submitted"
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                target_form_details_df.to_csv(
                    path_or_buf=path_out.joinpath("target_form_details_df.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            suppression_page_details_df = suppression_page_details_dataframe[
                (
                    suppression_page_details_dataframe["detail_dttm_tz"]
                    > str(suppression_hour_datetime)
                )
                & (
                    suppression_page_details_dataframe["detail_dttm_tz"]
                    <= str(current_hour_datetime)
                )
                & (
                    suppression_page_details_dataframe["domain_nm"]
                    == "support.worldwildlife.org"
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                suppression_page_details_df.to_csv(
                    path_or_buf=path_out.joinpath("suppression_page_details_df.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            suppression_form_details_df = suppression_form_details_dataframe[
                (
                    ~suppression_form_details_dataframe.detail_id.isin(
                        suppression_page_details_df.detail_id
                    )
                )
                & (
                    ~suppression_form_details_dataframe.identity_id.isin(
                        suppression_page_details_df.identity_id
                    )
                )
                & (
                    suppression_form_details_dataframe["form_field_detail_dttm_tz"]
                    > str(suppression_hour_datetime)
                )
                & (
                    suppression_form_details_dataframe["form_field_detail_dttm_tz"]
                    <= str(current_hour_datetime)
                )
                & (
                    suppression_form_details_dataframe["attempt_status_cd"]
                    == "3_Submitted Successfully"
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                suppression_form_details_df.to_csv(
                    path_or_buf=path_out.joinpath("suppression_form_details_df.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            target_df = target_form_details_df[
                (
                    ~target_form_details_df.identity_id.isin(
                        suppression_form_details_df.identity_id
                    )
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                target_df.to_csv(
                    path_or_buf=path_out.joinpath("target_df.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            suppression_df_is_valid_email = target_df[
                (target_df.identity_id.isin(customer_datamart_dataframe.identity_id))
            ]

            if flag_test_export is True and flag_test_report is True:
                suppression_df_is_valid_email.to_csv(
                    path_or_buf=path_out.joinpath("suppression_df_is_valid_email.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            result_dataframe = suppression_df_is_valid_email[
                (
                    ~suppression_df_is_valid_email.email.isin(
                        suppression_email_domain_list
                    )
                )
            ]

            if flag_test_export is True and flag_test_report is True:
                result_dataframe.to_csv(
                    path_or_buf=path_out.joinpath("result_dataframe.csv"),
                    sep=",",
                    index=False,
                    header=False,
                )

            if flag_test_report is True:
                result_dataframe = result_dataframe[
                    ["identity_id", "email", "form_field_detail_dttm_tz"]
                ]
            else:
                result_dataframe = result_dataframe[["identity_id", "email"]]

            result_out_dataframe = result_dataframe
            result_out_dataframe.insert(0, "eventName", "CART_Email_Event")
            result_out_dataframe.insert(1, "entityName", "visitor_id")
            result_out_dataframe.insert(
                2, "entityValue", result_dataframe["identity_id"]
            )
            result_out_dataframe.insert(3, "attrName1", "taskName")
            result_out_dataframe.insert(
                4, "attrValue1", "CART_Donations_Triggered_Email"
            )
            result_out_dataframe.insert(5, "attrName2", "emailAddress")
            result_out_dataframe.insert(6, "attrValue2", result_dataframe["email"])
            if flag_test_export is True and flag_test_report is True:
                result_out_dataframe.insert(7, "attrName3", "form_field_detail_dttm_tz")
                result_out_dataframe.insert(
                    8, "attrValue3", result_dataframe["form_field_detail_dttm_tz"]
                )
            if flag_test_export is True and flag_test_report is True:
                result_out_dataframe = result_out_dataframe.drop(
                    columns=["identity_id", "email", "form_field_detail_dttm_tz"]
                )
            else:
                result_out_dataframe = result_out_dataframe.drop(
                    columns=["identity_id", "email"]
                )
            result_out_dataframe.to_csv(
                path_or_buf=path_out, sep=",", index=False, header=False
            )

            flag_test_export = self._flag_test_export
            self.logger.info(msg=flag_test_export)

            if flag_test_export is True:
                email_list = Path(
                    root_path + self._export_test_path + self._export_test_file
                )
            else:
                email_list = Path(
                    root_path + self._export_prod_path + self._export_prod_file
                )
            self.logger.info(msg=email_list)

            # TODO: The following code appears to be incomplete/broken and causes undefined name errors
            # response = post_bulk_load_external_events
            # url_put = kwargs["url_put"]
            # json_post = kwargs["json_post"]
            # for items in json_post["links"]:
            #     url_put = items["href"]
            # result = self.put_file_location(self, result, json_post=json_post)
        except (AttributeError, Exception) as e:
            self.logger.exception("Exception occurred: {}".format(str(e)))
        finally:
            return


if __name__ == "__main__":
    BuildEmailData.__init__(BuildEmailData())
