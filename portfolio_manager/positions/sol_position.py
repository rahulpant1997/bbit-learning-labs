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

from implementations.security_solution import Security
from interfaces.position_interface import PositionInterface
from interfaces.security_interface import SecurityInterface


class Position(PositionInterface):
    def __init__(self, security_in, initial_position: int) -> None:
        super().__init__(security_in, initial_position)
        self.position_value = initial_position

        if isinstance(security_in, SecurityInterface):
            self.security = security_in
        else:
            self.security = Security(security_in)

    def get_security(self) -> SecurityInterface:
        return self.security

    def get_position(self) -> int:
        return self.position_value

    def set_position(self, input_value: int) -> None:
        if input_value < 0:
            raise Exception("Position update would cause a short position!")
        self.position_value = input_value

    def add_position(self, input_value: int) -> None:
        if self.position_value + input_value < 0:
            raise Exception("Position update would cause a short position!")

        self.position_value += input_value
