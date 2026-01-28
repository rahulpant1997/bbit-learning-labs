# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from asyncio import sleep

module_path = os.path.abspath("..")
if module_path not in sys.path:
    sys.path.append(module_path)
from datetime import datetime

import pytest
from generators.priceDataGenerator import priceData
from implementations.securitySolution import security


def test_getNearestTimeMarketValue():
    # GIVEN
    EXPECTED_NAME = "IBM US Equity"
    SLEEP_TIME = 0.5
    TIMED_COUNTS = 5
    TIME_VALUES = {}

    # WHEN
    testObj = security(EXPECTED_NAME)
    while TIMED_COUNTS > 0:
        curTimedPrice = testObj.getCurrentSecurityValue()
        sleep(0.1)
        TIME_VALUES[datetime.now()] = curTimedPrice
        TIMED_COUNTS -= 1
        sleep(SLEEP_TIME)

    # EXPECT
    for keys in TIME_VALUES:
        assert testObj.getSecurityValueAtTime(keys) == TIME_VALUES[keys]
