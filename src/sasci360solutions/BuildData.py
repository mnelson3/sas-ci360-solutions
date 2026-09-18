# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
import datetime
import logging
import os
from datetime import timedelta
from pathlib import Path

import pandas

from standard import Standard, root_path


class BuildData:

    def __init__(self):
        log_file = Path(root_path + Standard.gDirLog + "discover-builddata.log")
        logger = logging.getLogger()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        standard = Standard.Standard()

        self._suppression_email_domain_list = standard.suppression_email_domain_list()
        self._suppression_form_name_list = standard.suppression_form_name_list()

    def suppression_email_domain_list(self, value=None):
        if value:
            self._suppression_email_domain_list = value
        try:
            return self._suppression_email_domain_list
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def suppression_form_name_list(self, value=None):
        if value:
            self._suppression_form_name_list = value
        try:
            return self._suppression_form_name_list
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None

    def build_email_list(self):
        try:
            suppression_email_domain_list = self.suppression_email_domain_list()
            suppression_form_name_list = self.suppression_form_name_list()

            today = pandas.to_datetime(datetime.datetime.now())
            current_hour_datetime = today.floor("H").to_pydatetime()

            suppression_hour = today + timedelta(hours=-1)
            suppression_hour_datetime = suppression_hour.floor("H").to_pydatetime()

            target_hour = today + timedelta(hours=-2)
            target_hour_datetime = target_hour.floor("H").to_pydatetime()

            path = Path(root_path + Standard.gDsDscClean)
            path_out = Path(
                root_path + Standard.gDsDscExport + Standard.gDsDscExportProdFile
            )
            form_details_dataframe = pandas.DataFrame()

            for filename in os.listdir(path=path):
                if str(filename).startswith("FORM_DETAILS"):
                    file_path = path.joinpath(filename)
                    form_details_dataframe = pandas.read_csv(
                        filepath_or_buffer=file_path,
                        sep="|",
                        delimiter="|",
                        encoding="UTF-8",
                    )

            target_data_dataframe = form_details_dataframe
            target_df = target_data_dataframe[
                (
                    target_data_dataframe["form_field_detail_dttm"]
                    > str(target_hour_datetime)
                )
                & (
                    target_data_dataframe["form_field_detail_dttm"]
                    <= str(suppression_hour_datetime)
                )
            ]
            target_df_eq_not_submit = target_df[
                (target_df["attempt_status_cd"] == "0_Not Submitted")
            ]
            target_df_eq_target_form = target_df_eq_not_submit[
                (target_df_eq_not_submit["form_nm"] == "Support: Donation Form")
            ]
            target_df_eq_target_email = target_df_eq_target_form[
                (target_df_eq_target_form["form_field_nm"] == "donor.email")
            ]
            target_df_is_not_null_email = target_df_eq_target_email[
                (target_df_eq_target_email["form_field_value"].notnull())
            ]
            target_df_is_not_invalid_email = target_df_is_not_null_email[
                (
                    ~target_df_is_not_null_email.form_field_nm.isin(
                        suppression_email_domain_list
                    )
                )
            ]

            suppression_data_dataframe = form_details_dataframe
            suppression_df = suppression_data_dataframe[
                (
                    suppression_data_dataframe["form_field_detail_dttm"]
                    > str(suppression_hour_datetime)
                )
                & (
                    suppression_data_dataframe["form_field_detail_dttm"]
                    <= str(current_hour_datetime)
                )
            ]
            suppression_df_eq_submit = suppression_df[
                (suppression_df["attempt_status_cd"] == "3_Submitted Successfully")
            ]
            suppression_df_eq_form = suppression_df_eq_submit[
                suppression_df_eq_submit.form_nm.isin(suppression_form_name_list)
            ]
            suppression_df_is_not_null_email = suppression_df_eq_form[
                (suppression_df_eq_form["form_field_value"].notnull())
            ]
            suppression_df_is_not_invalid_email = suppression_df_is_not_null_email[
                (
                    ~suppression_df_is_not_null_email.form_field_nm.isin(
                        suppression_email_domain_list
                    )
                )
            ]

            result_dataframe = target_df_is_not_null_email[
                ~target_df_is_not_invalid_email.form_field_value.isin(
                    suppression_df_is_not_invalid_email["form_field_value"]
                )
            ]
            print(result_dataframe)
            result_dataframe = result_dataframe[["identity_id", "form_field_value"]]
            print(result_dataframe)

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
            result_out_dataframe.insert(
                6, "attrValue2", result_dataframe["form_field_value"]
            )

            result_out_dataframe = result_out_dataframe.drop(
                columns=["identity_id", "form_field_value"]
            )

            result_out_dataframe.to_csv(
                path_or_buf=path_out, sep=",", index=False, header=False
            )
        except Exception as e:
            logging.exception("Exception occurred: " + str(e))
            return None
        finally:
            return


if __name__ == "__main__":
    BuildData.__init__(BuildData())
