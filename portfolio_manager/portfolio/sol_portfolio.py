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

# Portfolio Class
from typing import Iterable, Set

from interfaces.account_interface import AccountInterface
from interfaces.portfolio_interface import PortfolioInterface


class Portfolio(PortfolioInterface):
    def __init__(
        self, portfolio_name: str, accounts: Set[AccountInterface]
    ) -> None:
        super().__init__(portfolio_name, accounts)
        self.name = portfolio_name
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
