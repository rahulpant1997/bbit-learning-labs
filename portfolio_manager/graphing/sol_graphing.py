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

from bqplot import pyplot as plt

module_path = os.path.abspath("..")
if module_path not in sys.path:
    sys.path.append(module_path)
from implementations.security_solution import Security


def create_security_mv(security_name, data_point_size):
    size = data_point_size
    security_obj = Security(security_name)
    market_values = {}
    count = 0
    while count < size:
        market_values[count] = security_obj.get_current_market_value()
        count += 1

    x_data = list(market_values.keys())
    y_data = list(market_values.values())

    plt.figure(title=security_obj.get_name(), animation_duration=1000)
    plt.plot(x_data, y_data)
    plt.show()
    return plt


plt = create_security_mv("IBM US Equity", 1000)
