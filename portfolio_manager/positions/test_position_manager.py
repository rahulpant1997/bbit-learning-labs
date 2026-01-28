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

import importlib

import implementations.position_solution
import pytest
from generators.position_data_generator import PositionUpdates
from implementations.security_solution import Security

importlib.reload(implementations.position_solution)


def test_position_manager_inits():
    # GIVEN
    expected_name = "DSAQ US Equity"
    expected_position = 1000
    input_sec = Security(expected_name)

    # WHEN
    test_obj_a = implementations.position_solution.Position(
        input_sec, expected_position
    )
    test_obj_b = implementations.position_solution.Position(
        expected_name, expected_position
    )

    # EXPECT
    assert test_obj_a.get_security().get_name() == expected_name
    assert test_obj_b.get_security().get_name() == expected_name
    assert test_obj_a.get_position() == expected_position
    assert test_obj_b.get_position() == expected_position


def test_position_updates():
    # GIVEN
    sec_data = PositionUpdates()
    expected_position = sum(sec_data.get_transaction_list())

    # WHEN
    test_obj = implementations.position_solution.Position("TEST", 0)
    for update in sec_data.get_transaction_list():
        test_obj.add_position(update)

    # EXPECT
    assert test_obj.get_position() == expected_position


def test_position_set():
    # GIVEN
    test_obj = implementations.position_solution.Position("TEST", 0)
    expected_position = 1000

    # WHEN
    test_obj.set_position(expected_position)

    # EXPECT
    assert test_obj.get_position() == expected_position


def test_position_update_short_block():
    # GIVEN
    base_position = 100
    update_position = -101
    test_obj = implementations.position_solution.Position("TEST", base_position)

    # EXPECT
    with pytest.raises(Exception):
        test_obj.add_position(update_position)
