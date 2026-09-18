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
