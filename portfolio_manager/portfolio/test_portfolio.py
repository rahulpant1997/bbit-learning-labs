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

import implementations.portfolio_solution
import pytest
from implementations.account_solution import Account
from implementations.position_solution import Position

importlib.reload(implementations.portfolio_solution)


def test_get_all_accounts():
    # GIVEN
    portfolio_name = "TestPortfolio"
    account_a_positions = [
        Position("MSFT US Equity", 1000),
        Position("TSLA US Equity", 2000),
    ]
    account_b_positions = [
        Position("APPL US Equity", 500),
        Position("RIVN US Equity", 1000),
    ]
    account_a = Account(account_a_positions, "Account A")
    account_b = Account(account_b_positions, "Account B")

    accounts = {account_a, account_b}
    expected_accounts = {acc.get_name(): True for acc in accounts}

    # WHEN
    p = implementations.portfolio_solution.Portfolio(portfolio_name, accounts)

    # EXPECT
    all_accs = p.get_all_accounts()

    for acc in all_accs:
        assert acc.get_name() in expected_accounts
        expected_accounts[acc.get_name()] = False

    assert True not in expected_accounts.values()


@pytest.mark.parametrize(
    "input_account, input_security, expected_map",
    (
        ([], [], {"Account A": True, "Account B": True, "Account C": True}),
        (
            ["Account A", "Account B", "Account DNE"],
            [],
            {"Account A": True, "Account B": True},
        ),
        (
            [],
            ["IBM US Equity", "FOOD US Equity"],
            {"Account A": True, "Account B": True, "Account C": True},
        ),
        (["Account B", "Account C"], ["IBM US Equity"], {"Account B": True}),
    ),
)
def test_get_subset_accounts(input_account, input_security, expected_map):
    # GIVEN
    portfolio_name = "TestPortfolio"
    account_a_positions = [
        Position("MSFT US Equity", 1000),
        Position("TSLA US Equity", 2000),
        Position("IBM US Equity", 3000),
    ]
    account_b_positions = [
        Position("APPL US Equity", 500),
        Position("RIVN US Equity", 1000),
        Position("IBM US Equity", 1234),
    ]
    account_c_positions = [
        Position("SWS US Equity", 241),
        Position("CORE US Equity", 4213),
        Position("FOOD US Equity", 1234),
    ]
    account_a = Account(account_a_positions, "Account A")
    account_b = Account(account_b_positions, "Account B")
    account_c = Account(account_c_positions, "Account C")

    accounts = {account_a, account_b, account_c}

    # WHEN
    p = implementations.portfolio_solution.Portfolio(portfolio_name, accounts)

    # EXPECT
    filtered_accounts = p.get_accounts(input_account, input_security)

    for acc in filtered_accounts:
        assert acc.get_name() in expected_map
        expected_map[acc.get_name()] = False

    assert True not in expected_map.values()


def test_add_accounts_no_overwrite():
    # GIVEN
    portfolio_name = "TestPortfolio"
    account_a_positions = [
        Position("MSFT US Equity", 1000),
        Position("TSLA US Equity", 2000),
    ]
    account_b_positions = [
        Position("APPL US Equity", 500),
        Position("RIVN US Equity", 1000),
    ]
    account_a = Account(account_a_positions, "Account A")
    account_b = Account(account_b_positions, "Account B")

    accounts = {account_a, account_b}
    expected_accounts = {acc.get_name(): True for acc in accounts}

    # WHEN
    p = implementations.portfolio_solution.Portfolio(portfolio_name, [])
    p.add_accounts(accounts)

    # EXPECT
    all_accs = p.get_all_accounts()

    for acc in all_accs:
        assert acc.get_name() in expected_accounts
        expected_accounts[acc.get_name()] = False

    assert True not in expected_accounts.values()


def test_add_account_overwrite():
    # GIVEN
    portfolio_name = "TestPortfolio"
    account_a_positions = [
        Position("MSFT US Equity", 1000),
        Position("TSLA US Equity", 2000),
    ]
    account_b_positions = [
        Position("APPL US Equity", 500),
        Position("RIVN US Equity", 1000),
    ]
    account_a = Account(account_a_positions, "Account A")
    account_b = Account(account_b_positions, "Account B")
    accounts = {account_a, account_b}

    # WHEN
    p = implementations.portfolio_solution.Portfolio(portfolio_name, accounts)
    account_b_positions_new = [
        Position("PELO US Equity", 500),
        Position("IBM US Equity", 1000),
    ]
    account_b_new = Account(account_b_positions_new, "Account B")
    expected_accounts = {
        "Account A": account_a_positions,
        "Account B": account_b_positions_new,
    }
    p.add_accounts([account_b_new])

    # EXPECT
    all_accs = p.get_all_accounts()

    for acc in all_accs:
        assert acc.get_name() in expected_accounts
        pos_expected = {
            x.get_security().get_name(): x.get_position()
            for x in expected_accounts[acc.get_name()]
        }
        return_pos = acc.get_all_positions()

        for pos in return_pos:
            assert pos.get_security().get_name() in pos_expected
            assert (
                pos_expected[pos.get_security().get_name()]
                == pos.get_position()
            )

            # Remove the validated Position from our expected map.
            del pos_expected[pos.get_security().get_name()]

        assert len(pos_expected) == 0


def test_remove_accounts():
    # GIVEN
    portfolio_name = "TestPortfolio"
    account_a_positions = [
        Position("MSFT US Equity", 1000),
        Position("TSLA US Equity", 2000),
    ]
    account_b_positions = [
        Position("APPL US Equity", 500),
        Position("RIVN US Equity", 1000),
    ]
    account_a = Account(account_a_positions, "Account A")
    account_b = Account(account_b_positions, "Account B")

    accounts = {account_a, account_b}
    expected_accounts = {"Account A": True}

    # WHEN
    p = implementations.portfolio_solution.Portfolio(portfolio_name, accounts)
    p.remove_accounts(["Account B", "Account DNE"])

    # EXPECT
    all_accs = p.get_all_accounts()

    for acc in all_accs:
        assert acc.get_name() in expected_accounts
        expected_accounts[acc.get_name()] = False

    assert True not in expected_accounts.values()
