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
from time import sleep, time

module_path = os.path.abspath("..")
if module_path not in sys.path:
    sys.path.append(module_path)
from datetime import datetime

import pytest
from implementations.positionSolution import position
from implementations.securitySolution import security


def test_securityTimedMarketValues():
    # GIVEN
    EXPECTED_NAME = "IBM US Equity"
    SLEEP_TIME = 0.005
    TIMED_COUNTS = 20
    TIME_VALUES = {}

    # WHEN
    testObj = security(EXPECTED_NAME)
    startTime = None
    endTime = None
    rangeMap = {}
    while TIMED_COUNTS > 0:
        curTimedPrice = testObj.getCurrentSecurityValue()
        timeKey = datetime.now()
        TIME_VALUES[timeKey] = curTimedPrice

        if TIMED_COUNTS == 15:
            startTime = timeKey

        if TIMED_COUNTS == 7:
            endTime = timeKey

        if TIMED_COUNTS <= 14 and TIMED_COUNTS >= 7:
            rangeMap[curTimedPrice] = None

        TIMED_COUNTS -= 1
        sleep(SLEEP_TIME)

    # EXPECT
    for keys in TIME_VALUES:
        assert testObj.getSecurityValueAtTime(keys) == TIME_VALUES[keys]

    timeSet = set(TIME_VALUES.keys())
    timeVals = testObj.getSecurityValueAtTimes(timeSet)

    for timeKey in timeVals:
        assert timeKey in TIME_VALUES
        assert TIME_VALUES[timeKey] == timeVals[timeKey]

    timeRange = testObj.getSecurityValuesInRange(startTime, endTime)

    assert len(rangeMap) == len(timeRange)
    checkCount = 0
    for timeA, timeB in zip(timeRange.values(), rangeMap.keys()):
        assert timeA == timeB
        checkCount += 1

    assert len(rangeMap) == checkCount


def test_PositionValuesOverTime():
    EXPECTED_NAME = "IBM US Equity"
    TIMED_COUNTS = 10
    SLEEP_TIME = 0.01
    POSITION_CHANGES = [100, -300, 400, 100, -200]
    TIME_VALUES = {}
    testObj = position(EXPECTED_NAME, 1000)

    while TIMED_COUNTS > 0:
        curTimedMV = testObj.get_position()
        timeKey = datetime.now()
        TIME_VALUES[timeKey] = curTimedMV

        if (
            TIMED_COUNTS <= 6
            and TIMED_COUNTS >= 2
            and len(POSITION_CHANGES) != 0
        ):
            testObj.updatePosition(POSITION_CHANGES[0])
            del POSITION_CHANGES[0]
        TIMED_COUNTS -= 1
        sleep(SLEEP_TIME)

    timeSet = set(TIME_VALUES.keys())
    posVals = testObj.getPositionValueAtTimes(timeSet)

    for posKey in posVals:
        assert posKey in TIME_VALUES
        assert TIME_VALUES[posKey] == posVals[posKey]


def test_PositionTimedMarketValuesInSet():
    # GIVEN
    EXPECTED_NAME = "IBM US Equity"
    SLEEP_TIME = 0.01
    TIMED_COUNTS = 20
    POSITION_CHANGES = [100, -300, 400, 100, -200]
    TIME_VALUES = {}

    # WHEN
    testObj = position(EXPECTED_NAME, 1000)
    while TIMED_COUNTS > 0:
        curTimedMV = testObj.getMarketValue()
        timeKey = datetime.now()
        TIME_VALUES[timeKey] = curTimedMV

        if (
            TIMED_COUNTS <= 12
            and TIMED_COUNTS >= 7
            and len(POSITION_CHANGES) != 0
        ):
            testObj.updatePosition(POSITION_CHANGES[0])
            del POSITION_CHANGES[0]

        TIMED_COUNTS -= 1
        sleep(SLEEP_TIME)

    # EXPECT
    timeSet = set(TIME_VALUES.keys())
    timeVals = testObj.getMarketValueAtTimes(timeSet)

    for timeKey in timeVals:
        assert timeKey in TIME_VALUES
        assert TIME_VALUES[timeKey] == timeVals[timeKey]


def test_PositionTimedMarketValuesInRange():
    # GIVEN
    EXPECTED_NAME = "TSLA US Equity"

    # WHEN
    testObj = position(EXPECTED_NAME, 1000)
    startTime = datetime.now()
    endTime = None
    rangeMap = {}

    curTimedMV = testObj.getMarketValue()
    rangeMap[curTimedMV] = None

    curTimedMV = testObj.getMarketValue()
    rangeMap[curTimedMV] = None

    rangeMap[testObj.updatePosition(100)] = None

    curTimedMV = testObj.getMarketValue()
    rangeMap[curTimedMV] = None

    sleep(0.01)
    endTime = datetime.now()

    # EXPECT
    timeRange = testObj.getMarketValuesInRange(startTime, endTime)
    assert len(rangeMap) == len(timeRange)
    print(rangeMap)
    checkCount = 0
    for timeA, timeB in zip(timeRange.values(), rangeMap.keys()):
        assert timeA == timeB
        checkCount += 1

    assert len(rangeMap) == checkCount
