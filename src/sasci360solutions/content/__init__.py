# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from sasci360solutions.main import Main


class Content(Main):
    """
    Content Module
    """

    def __init__(self) -> None:
        super().__init__()

        print("Content-Result: {}".format(self.algorithm))


if __name__ == "__main__":
    Content()
