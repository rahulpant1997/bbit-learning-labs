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
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pika  # pylint: disable=import-error
from rmq_interfaces.producer_interface import ProducerInterface


class MQProducer(
    ProducerInterface
):  # pylint: disable=too-many-instance-attributes
    """Defines an interface for a Producer."""

    def __init__(
        self, routing_key: str, pub_delay: int, message_producer: Any
    ) -> None:
        self.routing_key = routing_key
        self.pub_delay = pub_delay
        self.pub_producer = message_producer
        self.run = threading.Event()
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.setup_rmq_connection()

    def __del__(self):
        print("Closing RMQ connection on destruction")
        self.connection.close()

    def setup_rmq_connection(self):
        con_params = pika.URLParameters(os.environ["AMQP_URL"])

        # Using blocking connection isn't safe across threads. Only use this within a single thread.
        # Our current threadpool has a max of 1 work.
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()

        # Create the exchange if not already present
        self.exchange = "RMQ Labs"
        self.channel.exchange_declare(self.exchange)

    def start_publishing(self):
        if self.run.is_set():
            print("Publishing thread started. No-op")
            return

        # Turn on our threading flag & start a thread which runs our publishing loop
        self.run.set()
        self.pool.submit(self.pub_loop)

    def stop_publishing(self):
        self.run.clear()
        print("Attempting to join pub thread")
        self.pool.shutdown()

    def pub_loop(self):
        while self.run.is_set():
            if self.pub_producer:
                data = self.pub_producer()
            else:
                data = (
                    f"The current time is {time.time()} in epoch time. "
                    f"Routing key is {self.routing_key}"
                )

            print(f"Submitting data message {data}")
            self.channel.basic_publish(
                self.exchange,
                self.routing_key,
                data,
                pika.BasicProperties(
                    content_type="text/plain",
                    delivery_mode=pika.DeliveryMode.Transient,
                ),
            )
            time.sleep(self.pub_delay)


test_obj = MQProducer("Test_Key", 1, None)
test_obj.start_publishing()
time.sleep(40)
test_obj.stop_publishing()
