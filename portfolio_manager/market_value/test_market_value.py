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
import implementations.portfolio_solution
import implementations.position_solution
import implementations.security_solution
from generators.price_data_generator import PriceData

importlib.reload(implementations.security_solution)
importlib.reload(implementations.position_solution)
importlib.reload(implementations.account_solution)


def create_portfolio_accounts():
    account_a_positions = [
        implementations.position_solution.Position("IBM US Equity", 530),
        implementations.position_solution.Position("TSLA US Equity", 1120),
        implementations.position_solution.Position("NVDA US Equity", 7421),
    ]

    account_b_positions = [
        implementations.position_solution.Position("IBM US Equity", 201),
        implementations.position_solution.Position("MSFT US Equity", 400),
        implementations.position_solution.Position("NVDA US Equity", 300),
        implementations.position_solution.Position("DLTA US Equity", 623),
    ]

    account_a = implementations.account_solution.Account(
        account_a_positions, "Account A"
    )
    account_b = implementations.account_solution.Account(
        account_b_positions, "Account B"
    )

    accounts = {"Account A": account_a, "Account B": account_b}

    return accounts


def test_security_value_gather():
    # GIVEN
    security_name = "TSLA US Equity"
    data_source = PriceData()
    data_source.clear_price_history()

    # WHEN
    test_obj = implementations.security_solution.Security(security_name)
    ## TODO: @Reviewers, we are calcualting MV and assigning it to price. This looks wrong.
    current_price = test_obj.get_current_market_value()

    # EXPECT
    assert (
        current_price
        == data_source.get_security_price_data_list(security_name)[-1]
    )


def test_position_market_value():
    # GIVEN
    expected_name = "IBM US Equity"
    expected_position_amount = 1000
    data_source = PriceData()
    data_source.clear_price_history()

    # WHEN
    test_obj = implementations.position_solution.Position(
        expected_name, expected_position_amount
    )
    MV = test_obj.get_current_market_value()
    lastest_expected_mv = (
        expected_position_amount
        * data_source.get_security_price_data_list(expected_name)[-1]
    )

    # EXPECT
    assert lastest_expected_mv == MV


def test_security_search_account_mv():
    # GIVEN
    data_source = PriceData()
    data_source.clear_price_history()
    expected_account_positions = [
        implementations.position_solution.Position("IBM US Equity", 530),
        implementations.position_solution.Position("TSLA US Equity", 1120),
        implementations.position_solution.Position("NVDA US Equity", 7421),
    ]
    search_securities_list = [
        "IBM US Equity",
        implementations.security_solution.Security("NVDA US Equity"),
        "MSFT US Equity",
    ]
    search_securities_tuple = [["IBM US Equity", 530], ["NVDA US Equity", 7421]]
    test_obj = implementations.account_solution.Account(
        expected_account_positions, "Test Account"
    )

    # WHEN
    market_Value = test_obj.get_current_filtered_market_value(
        search_securities_list
    )
    expected_mv = 0
    for sec_tuple in search_securities_tuple:
        if sec_tuple[1] != 0:
            expected_mv += (
                sec_tuple[1]
                * data_source.get_security_price_data_list(sec_tuple[0])[-1]
            )
    # EXPECT
    assert expected_mv == market_Value


def test_total_account_mv():
    # GIVEN
    expected_account_positions = [
        implementations.position_solution.Position("IBM US Equity", 530),
        implementations.position_solution.Position("TSLA US Equity", 1120),
        implementations.position_solution.Position("NVDA US Equity", 7421),
    ]
    data_source = PriceData()
    data_source.clear_price_history()
    test_obj = implementations.account_solution.Account(
        expected_account_positions, "Test Account"
    )

    # WHEN
    market_value = test_obj.get_current_market_value()
    expected_mv = 0
    for pos in expected_account_positions:
        expected_mv += (
            pos.get_position()
            * data_source.get_security_price_data_list(
                pos.get_security().get_name()
            )[-1]
        )
    # EXPECT
    assert expected_mv == market_value


def test_total_portfolio_mv():
    portfolio_name = "TestPortfolio"
    accounts = create_portfolio_accounts()
    position_map_total = {}

    for acc in accounts.values():
        for pos in acc.get_all_positions():
            if pos.get_security().get_name() in position_map_total:
                position_map_total[pos.get_security().get_name()].add_position(
                    pos.get_position()
                )
            else:
                position_map_total[pos.get_security().get_name()] = (
                    implementations.position_solution.Position(
                        pos.get_security(), pos.get_position()
                    )
                )

    data_source = PriceData()
    data_source.clear_price_history()
    test_obj = implementations.portfolio_solution.Portfolio(
        portfolio_name, accounts.values()
    )

    mv_total = test_obj.get_current_market_value()
    expected_mv_total = 0
    for pos in position_map_total.values():
        expected_mv_total += (
            pos.get_position()
            * data_source.get_security_price_data_list(
                pos.get_security().get_name()
            )[-1]
        )
    assert mv_total == expected_mv_total


def test_filtered_portfolio_mvs():
    # GIVEN
    portfolio_name = "TestPortfolio"
    accounts = create_portfolio_accounts()

    position_map_total_acc = {}
    position_map_total_security = {}
    position_map_total_security_acc = {}
    security_filter = "IBM US Equity"
    acc_filter = "Account B"
    for acc in accounts.values():
        for pos in acc.get_all_positions():
            if pos.get_security().get_name() == security_filter:
                if pos.get_security().get_name() in position_map_total_security:
                    position_map_total_security[
                        pos.get_security().get_name()
                    ].add_position(pos.get_position())
                else:
                    position_map_total_security[
                        pos.get_security().get_name()
                    ] = implementations.position_solution.Position(
                        pos.get_security().get_name(), pos.get_position()
                    )

            if acc.get_name() == acc_filter:
                if pos.get_security().get_name() in position_map_total_acc:
                    position_map_total_acc[
                        pos.get_security().get_name()
                    ].add_position(pos.get_position())
                else:
                    position_map_total_acc[pos.get_security().get_name()] = (
                        implementations.position_solution.Position(
                            pos.get_security().get_name(), pos.get_position()
                        )
                    )

                if pos.get_security().get_name() == security_filter:
                    if (
                        pos.get_security().get_name()
                        in position_map_total_security_acc
                    ):
                        position_map_total_security_acc[
                            pos.getSecurityName()
                        ].add_position(pos.get_position())
                    else:
                        position_map_total_security_acc[
                            pos.get_security().get_name()
                        ] = implementations.position_solution.Position(
                            pos.get_security().get_name(), pos.get_position()
                        )

    data_source = PriceData()
    data_source.clear_price_history()
    test_obj = implementations.portfolio_solution.Portfolio(
        portfolio_name, accounts.values()
    )

    # WHEN
    mv_acc = test_obj.get_current_filtered_market_value([acc_filter], [])
    expected_mv_acc = 0
    for pos in position_map_total_acc.values():
        expected_mv_acc += (
            pos.get_position()
            * data_source.get_security_price_data_list(
                pos.get_security().get_name()
            )[-1]
        )
    data_source = PriceData()
    data_source.clear_price_history()

    mv_security = test_obj.get_current_filtered_market_value(
        [], [security_filter]
    )
    expected_mv_security = 0
    for pos in position_map_total_security.values():
        expected_mv_security += (
            pos.get_position()
            * data_source.get_security_price_data_list(
                pos.get_security().get_name()
            )[-1]
        )
    data_source = PriceData()
    data_source.clear_price_history()

    mv_acc_security = test_obj.get_current_filtered_market_value(
        [acc_filter], [security_filter]
    )
    expected_mv_acc_security = 0
    for pos in position_map_total_security_acc.values():
        expected_mv_acc_security += (
            pos.get_position()
            * data_source.get_security_price_data_list(
                pos.get_security().get_name()
            )[-1]
        )
    data_source = PriceData()
    data_source.clear_price_history()

    # EXPECT
    assert mv_acc == expected_mv_acc
    assert mv_acc_security == expected_mv_acc_security
    assert mv_security == expected_mv_security
