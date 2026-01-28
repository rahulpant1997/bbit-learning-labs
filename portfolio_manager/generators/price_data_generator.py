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

import random


class PriceData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PriceData, cls).__new__(cls)
            cls._instance.__security_price_data = {}
            cls._instance.__security_rally = {}
        return cls._instance

    def __identify_security_type(self, security_name: str) -> bool:
        # Check if the security only makes sense to have positive values
        if (
            "eqty" in security_name.casefold()
            or "equity" in security_name.casefold()
        ):
            return True

        return False

    def get_current_price(self, security_name: str) -> float:
        positive_only = self.__identify_security_type(security_name)

        if security_name not in self.__security_price_data:
            self.__security_price_data[security_name] = []

        if positive_only:
            # Check if we need seed position
            if len(self.__security_price_data[security_name]) == 0:
                self.__security_price_data[security_name].append(
                    random.choices(range(0, 10000))[0]
                )
            else:
                # Check if we hit a rally
                if (
                    len(self.__security_price_data[security_name]) > 2
                    and self.__security_price_data[security_name][-1]
                    - self.__security_price_data[security_name][-2]
                    > 0
                    and random.uniform(0, 1) < 0.0005
                    and security_name not in self.__security_rally
                ):
                    self.__security_rally[security_name] = 10

                if security_name in self.__security_rally:
                    security_move = self.__security_price_data[security_name][
                        -1
                    ] * random.uniform(0.05, 0.1)
                    self.__security_rally[security_name] -= 1
                    if self.__security_rally[security_name] <= 0:
                        del self.__security_rally[security_name]
                    self.__security_price_data[security_name].append(
                        self.__security_price_data[security_name][-1]
                        + security_move
                    )
                else:
                    # Generate a move positive or negative. With a percentage move
                    security_move = self.__security_price_data[security_name][
                        -1
                    ] * random.uniform(0.0001, 0.01)

                if bool(random.getrandbits(1)):
                    self.__security_price_data[security_name].append(
                        self.__security_price_data[security_name][-1]
                        + security_move
                    )
                else:
                    self.__security_price_data[security_name].append(
                        self.__security_price_data[security_name][-1]
                        - security_move
                    )
        else:
            self.__security_price_data[security_name].append(
                random.choices(range(-2000, 10000))[0]
            )

        return self.__security_price_data[security_name][-1]

    def get_price_data_list(self) -> dict:
        return self.__security_price_data

    def get_security_price_data_list(self, security_name: str) -> list:
        return self.__security_price_data[security_name]

    def clear_price_history(self) -> None:
        self.__security_price_data = {}
