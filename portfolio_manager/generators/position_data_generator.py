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

# TODO We should probably place this in it's own ENG Provider Package
# Should we allow for negative net positions?
import random


class PositionUpdates:
    def __init__(self) -> None:
        self.__security_transactions_size = 10
        self.__current_transaction_position = 0
        self.__security_transactions = self.__generate_transaction_list(
            self.__security_transactions_size
        )

    def __generate_transaction_list(self, transaction_size: int) -> list[int]:
        if transaction_size <= 0:
            raise Exception(
                f"Unable to generate position transactions. Size given is negative. Size:{transaction_size}"
            )

        count = 0
        current_position_count = 0
        transaction_list = []
        while count < transaction_size:
            if count == 0:
                pos_update = random.randint(1, 1001)
            else:
                pos_update = random.randint(-400, 1001)
                while current_position_count + pos_update < 0:
                    pos_update = random.randint(-400, 1001)

            transaction_list.append(pos_update)
            current_position_count += pos_update
            count += 1

        return transaction_list

    def get_transaction_list(self) -> list:
        return self.__security_transactions

    def get_next_transaction(self) -> int:
        if (
            self.__current_transaction_position
            >= self.__security_transactions_size
        ):
            raise Exception("No more transaction available")

        rtn = self.__security_transactions[self.__current_transaction_position]
        self.__current_transaction_position += 1
        return rtn

    def is_next_available(self) -> bool:
        return (
            self.__current_transaction_position
            < self.__security_transactions_size
        )
