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

from typing import Iterable, Set

from interfaces.account_interface import AccountInterface
from interfaces.portfolio_interface import PortfolioInterface


class Portfolio(PortfolioInterface):
    def __init__(
        self, portfolioName: str, accounts: Set[AccountInterface]
    ) -> None:
        super().__init__(portfolioName, accounts)
        self.name = portfolioName
        self.accounts = {acc_item.get_name(): acc_item for acc_item in accounts}

    def get_all_accounts(self) -> Iterable[AccountInterface]:
        return list(self.accounts.values())

    def get_accounts(
        self, account_names_filter: Set[str], securities_filter: Set
    ) -> Iterable[AccountInterface]:
        if len(account_names_filter) == 0 and len(securities_filter) == 0:
            return self.get_all_accounts()

        if len(account_names_filter) != 0:
            filtered_acc = set()

            for acc in account_names_filter:
                if acc in self.accounts:
                    filtered_acc.add(self.accounts[acc])
        else:
            filtered_acc = set(self.accounts.values())

        final_set = set()
        if len(securities_filter) != 0:
            for acc in filtered_acc:
                if len(acc.get_positions(securities_filter)) != 0:
                    final_set.add(acc)
        else:
            final_set = filtered_acc

        return final_set

    def add_accounts(self, accounts: Set[AccountInterface]) -> None:
        for accounts in accounts:
            self.accounts[accounts.get_name()] = accounts

    def remove_accounts(self, account_names: Set[str]) -> None:
        for acc_name in account_names:
            self.accounts.pop(acc_name, None)

    def __aggregate_account_market_value(
        self, accounts: Iterable[AccountInterface]
    ):
        # Aggregate positions at this level & query their security value.
        aggregate_pos_map = {}
        for account in accounts:
            for position in account.get_all_positions():
                if position.get_security().get_name() in aggregate_pos_map:
                    aggregate_pos_map[position.get_security().get_name()][
                        0
                    ] += position.get_position()
                else:
                    # List with reference to underlying security
                    aggregate_pos_map[position.get_security().get_name()] = [
                        position.get_position(),
                        position.get_security(),
                    ]

        summed_market_value = 0
        for pos_tuple in aggregate_pos_map.values():
            summed_market_value += (
                pos_tuple[0] * pos_tuple[1].get_current_market_value()
            )

        return summed_market_value

    def get_current_market_value(self) -> dict:
        return self.__aggregate_account_market_value(self.accounts.values())

    def get_current_filtered_market_value(
        self, securities: Set, account_names: Set[str]
    ) -> float:
        return self.__aggregate_account_market_value(
            self.get_accounts(account_names, securities)
        )
