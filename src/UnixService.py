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
import time
from logging.handlers import SysLogHandler

from service import Service, find_syslog

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class UnixService(Service):
    POLL_INTERVAL_SECONDS = 300

    def __init__(self, *args, **kwargs):
        super(UnixService, self).__init__(*args, **kwargs)
        self.logger.addHandler(
            SysLogHandler(address=find_syslog(), facility=SysLogHandler.LOG_DAEMON)
        )
        self.logger.setLevel(logging.INFO)

    def run(self):
        from sasci360solutions.main import CI360Main

        app = CI360Main()
        while not self.got_sigterm():
            try:
                app.check_and_run()
            except Exception as e:
                self.logger.exception("Exception occurred: {}".format(str(e)))
            time.sleep(self.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit("Syntax: %s COMMAND" % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = UnixService("SAS_CI360_Service", pid_dir="/tmp")  # nosec B108

    if cmd == "start":
        service.start()
    elif cmd == "stop":
        service.stop()
    elif cmd == "status":
        if service.is_running():
            print("Service is running.")
        else:
            print("Service is not running.")
    else:
        sys.exit('Unknown command "%s".' % cmd)
