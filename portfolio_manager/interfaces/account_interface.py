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

"""Defines the class interface for Account."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Set

from .position_interface import PositionInterface


class AccountInterface(ABC):
    """Defines the structure of a Account class."""

    @abstractmethod
    def __init__(
        self, positions: Set[PositionInterface], account_name: str
    ) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_all_positions(self) -> Iterable[PositionInterface]:
        pass

    @abstractmethod
    def get_positions(self, securities: Set) -> Dict[Any, PositionInterface]:
        pass

    @abstractmethod
    def add_positions(self, positions: Set[PositionInterface]) -> None:
        pass

    @abstractmethod
    def remove_positions(self, securities: Set) -> None:
        pass
