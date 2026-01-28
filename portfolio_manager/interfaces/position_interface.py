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

"""Position Class Interface."""

from abc import ABC, abstractmethod

from .security_interface import SecurityInterface


class PositionInterface(ABC):
    """Defines the structure of a Position class."""

    def __init__(self, security, initial_position: int) -> None:
        pass

    @abstractmethod
    def get_security(self) -> SecurityInterface:
        pass

    @abstractmethod
    def get_position(self) -> int:
        pass

    @abstractmethod
    def set_position(self, input_value: int) -> None:
        pass

    @abstractmethod
    def add_position(self, input_value: int) -> None:
        pass
