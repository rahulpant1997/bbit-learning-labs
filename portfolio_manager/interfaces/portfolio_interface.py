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

"""Defines the class interface for Portfolio."""

from abc import ABC, abstractmethod
from typing import Iterable, Set

from .account_interface import AccountInterface


class PortfolioInterface(ABC):
    """Defines the structure of a Portfolio class."""

    @abstractmethod
    def __init__(
        self, portfolio_name: str, accounts: Set[AccountInterface]
    ) -> None:
        pass

    @abstractmethod
    def get_all_accounts(self) -> Iterable[AccountInterface]:
        pass

    @abstractmethod
    def get_accounts(
        self, account_names_filter: Set[str], securities_filter: Set
    ) -> Iterable[AccountInterface]:
        pass

    @abstractmethod
    def add_accounts(self, accounts: Set[AccountInterface]) -> None:
        pass

    @abstractmethod
    def remove_accounts(self, account_names: Set[str]) -> None:
        pass
