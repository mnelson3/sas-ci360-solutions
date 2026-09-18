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
import socket
import sys
from pathlib import Path

import servicemanager
from win32 import win32event, win32service
from win32.lib import win32serviceutil


class SASCI360Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "SASCI360Service"
    _svc_display_name_ = "SAS CI360 Service"
    _svc_description_ = (
        "Windows Service used to run SAS CI360 Automation Engine as a service."
    )

    _current_file_ = __file__
    _real_path_ = os.path.realpath(_current_file_)
    _dir_path_ = os.path.dirname(_real_path_)
    _dir_name_ = os.path.basename(_dir_path_)
    _src_path_ = os.path.abspath(os.path.join(_dir_path_, os.pardir))
    _root_path_ = os.path.abspath(os.path.join(_src_path_, os.pardir))
    sys.path.append(_dir_path_)

    def __init__(self, *args):
        log_file = Path("{0}{1}{2}".format(self._src_path_, "/logs/", "service.log"))
        logger = logging.getLogger()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        win32serviceutil.ServiceFramework.__init__(self, args[0])
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
        except Exception as e:
            logging.exception("Exception occurred: {}".format(str(e)))
            return None

    def SvcDoRun(self):
        try:
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, ""),
            )
            self.main()
        except Exception as e:
            logging.exception("Exception occurred: {}".format(str(e)))
            return None

    def main(self):
        try:
            src_path = Path(self._dir_path_.format("/main"))
            sys.path.append(src_path)
            from main import Main

            rc = None
            while rc != win32event.WAIT_OBJECT_0:
                Main.start()
                rc = win32event.WaitForSingleObject(self.hWaitStop, 50000)
        except Exception as e:
            logging.exception("Exception occurred: {}".format(str(e)))
            return None


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(SASCI360Service)

# =================================================================================================================
# python SASCI360Service.py install
# python SASCI360Service.py remove
#
# Usage: "SASCI360Service.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]"
# Options for "install" and "update" commands only:
#  --username domain\username : The Username the service is to run under
#  --password password : The password for the username
#  --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
#  --interactive : Allow the service to interact with the desktop.
#  --perfmonini file: .ini file to use for registering performance monitor data
#  --perfmondll file: .dll file to use when querying the service for
#    performance data, default = perfmondata.dll
# Options for "start" and "stop" commands only:
#  --wait seconds: Wait for the service to actually start or stop.
#                  If you specify --wait with the "stop" option, the service
#                  and all dependent services will be stopped, each waiting
#                  the specified period.
# =================================================================================================================
