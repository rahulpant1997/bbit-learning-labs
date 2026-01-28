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

import implementations.account_solution
from implementations.position_solution import Position
from implementations.security_solution import Security

importlib.reload(implementations.account_solution)


def test_get_account_name():
    # GIVEN
    expected_name = "MY TEST ACCOUNT"
    expected_positions = set()

    # WHEN
    test_obj = implementations.account_solution.Account(
        expected_positions, expected_name
    )

    # EXPECT
    assert test_obj.get_name() == expected_name


def test_get_all_positions():
    # GIVEN
    expected_name = "MY TEST ACCOUNT"
    expected_positions = set()
    expected_positions.add(Position("TEST_SEC_A", 1000))
    expected_positions.add(Position("TEST_SEC_B", 2000))

    # WHEN
    test_obj = implementations.account_solution.Account(
        expected_positions, expected_name
    )
    return_pos_itr = test_obj.get_all_positions()

    # EXPECT
    assert len(return_pos_itr) == len(expected_positions)

    for item in list(return_pos_itr):
        assert item in expected_positions
        expected_positions.remove(item)
        return_pos_itr.remove(item)

    assert len(return_pos_itr) == 0
    assert len(expected_positions) == 0


def test_get_positions():
    # GIVEN
    expected_name = "MY TEST ACCOUNT"
    expected_positions = set()
    expected_positions.add(Position("TEST_SEC_A", 1000))
    expected_positions.add(Position("TEST_SEC_B", 2000))
    key_list = [
        Security("TEST_SEC_A"),
        "TEST_SEC_B",
        "TEST_NOT_FOUND_STR",
        Security("TEST_NOT_FOUND_POS"),
    ]
    expected_map = {
        key_list[0]: Position("TEST_SEC_A", 1000),
        key_list[1]: Position("TEST_SEC_B", 2000),
    }

    # WHEN
    test_obj = implementations.account_solution.Account(
        expected_positions, expected_name
    )
    return_pos_itr = test_obj.get_positions(key_list)

    # EXPECT
    assert len(return_pos_itr) == len(key_list) - 2
    for item in key_list:
        if isinstance(item, Security) and "NOT_FOUND" in item.get_name():
            assert item not in return_pos_itr
        elif isinstance(item, str) and "NOT_FOUND" in item:
            assert item not in return_pos_itr
        else:
            assert item in return_pos_itr
            assert (
                return_pos_itr[item].get_security().get_name()
                == expected_map[item].get_security().get_name()
            )
            assert (
                return_pos_itr[item].get_position()
                == expected_map[item].get_position()
            )


def test_add_positions():
    expected_name = "MY TEST ACCOUNT"
    start_positions = {
        Position("TEST_SEC_A", 1000),
        Position("TEST_SEC_B", 2000),
    }
    update_positions = {
        Position("TEST_SEC_B", 3000),
        Position("TEST_SEC_C", 1500),
    }
    expected_positions = {
        "TEST_SEC_A": 1000,
        "TEST_SEC_B": 3000,
        "TEST_SEC_C": 1500,
    }

    # WHEN
    test_obj = implementations.account_solution.Account(
        start_positions, expected_name
    )
    test_obj.add_positions(update_positions)
    return_pos_itr = test_obj.get_all_positions()

    # EXPECT
    assert len(return_pos_itr) == len(expected_positions)

    for item in list(return_pos_itr):
        assert item.get_security().get_name() in expected_positions
        assert (
            item.get_position()
            == expected_positions[item.get_security().get_name()]
        )
        del expected_positions[item.get_security().get_name()]
        return_pos_itr.remove(item)

    assert len(return_pos_itr) == 0
    assert len(expected_positions) == 0


def test_removePositions():
    expected_name = "MY TEST ACCOUNT"
    start_positions = {
        Position("TEST_SEC_A", 1000),
        Position("TEST_SEC_B", 2000),
        Position("TEST_SEC_C", 1500),
        Position("TEST_SEC_D", 3500),
    }
    remove_positions = {Security("TEST_SEC_B"), Security("TEST_SEC_C")}
    expected_positions = {"TEST_SEC_A": 1000, "TEST_SEC_D": 3500}

    # WHEN
    test_obj = implementations.account_solution.Account(
        start_positions, expected_name
    )
    test_obj.remove_positions(remove_positions)
    return_pos_itr = test_obj.get_all_positions()

    # EXPECT
    assert len(return_pos_itr) == len(expected_positions)

    for item in list(return_pos_itr):
        assert item.get_security().get_name() in expected_positions
        assert (
            item.get_position()
            == expected_positions[item.get_security().get_name()]
        )
        del expected_positions[item.get_security().get_name()]
        return_pos_itr.remove(item)

    assert len(return_pos_itr) == 0
    assert len(expected_positions) == 0
