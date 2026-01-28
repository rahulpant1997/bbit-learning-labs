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

from typing import Any, Dict, Iterable, Set

from interfaces.account_interface import AccountInterface
from interfaces.position_interface import PositionInterface
from interfaces.security_interface import SecurityInterface


class Account(AccountInterface):
    def __init__(
        self, positions: Set[PositionInterface], account_name: str
    ) -> None:
        self.account_name = account_name
        self.positions = {
            pos_item.get_security().get_name(): pos_item
            for pos_item in positions
        }

    def get_name(self) -> str:
        return self.account_name

    def get_all_positions(self) -> Iterable[PositionInterface]:
        return list(self.positions.values())

    def get_positions(self, securities: Set) -> Dict[Any, PositionInterface]:
        return_postion_map = {}

        for security_key in securities:
            if (
                isinstance(security_key, SecurityInterface)
                and security_key.get_name() in self.positions
            ):
                return_postion_map[security_key] = self.positions[
                    security_key.get_name()
                ]
            elif security_key in self.positions:
                return_postion_map[security_key] = self.positions[security_key]

        return return_postion_map

    def add_positions(self, positions: Set[PositionInterface]) -> None:
        for position_itr in positions:
            if position_itr.get_security().get_name() in self.positions:
                self.positions[
                    position_itr.get_security().get_name()
                ].set_position(position_itr.get_position())
            else:
                self.positions[position_itr.get_security().get_name()] = (
                    position_itr
                )

    def remove_positions(self, securities: Set) -> None:
        for securityKey in securities:
            if isinstance(securityKey, SecurityInterface):
                self.positions.pop(securityKey.get_name(), None)
            else:
                self.positions.pop(securityKey, None)
