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
from pathlib import Path

from sasci360solutions.main import Main

current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
src_path = os.path.abspath(os.path.join(dir_path, os.pardir))
root_path = os.path.abspath(os.path.join(src_path, os.pardir))
pkg_path = os.path.abspath(os.path.join(root_path, os.pardir))
sys.path.append(dir_path)


class Planning(Main):
    """
    Planning Module
    """

    def __init__(self) -> None:
        super().__init__()

        self._log_file = Path("{0}{1}{2}".format(pkg_path, "/logs/", "root.log"))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        Path(self._log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(self._log_file)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        result = self.root.get_root()

        # algorithm = self.algorithm
        # print("Planning-Result: {}".format(algorithm))

        # self.call_get_root()
        print("Result B: {0}".format(result.status_code))
        print("Result B: {0}".format(result.json()))

    # def call_get_root(self) -> requests.Response:
    # 	"""
    # 	Get the links for the API
    # 	:return: Returns the links to the top-level resources for the API.
    # 	:rtype: requests.Response
    # 	"""
    # 	result = None
    # 	try:
    # 		result = self.root.get_root()
    # 		# print("Result A: {0}".format(result.status_code))
    # 	except (AttributeError, Exception) as e:
    # 		self.logger.exception("Exception occurred: {}".format(str(e)))
    # 	finally:
    # 		return result


if __name__ == "__main__":
    Planning()
