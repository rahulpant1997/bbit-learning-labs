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
import time
from concurrent.futures import ThreadPoolExecutor

import pika  # pylint: disable=import-error
from rmq_interfaces.consumer_interface import ConsumerInterface


class MQConsumer(ConsumerInterface):
    """An implementation of a Consumer."""

    def __init__(self, routing_key: str, **kwargs) -> None:
        self.routing_key = routing_key
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.message_handler = kwargs.get("messageHandler")
        self.setup_rmq_connection()

    def __del__(self):
        print("Closing RMQ connection on destruction")
        self.connection.close()

    def setup_rmq_connection(self):
        con_params = pika.URLParameters(os.environ["AMQP_URL"])

        # Using blocking connection isn't safe across threads. Only use this within a single thread.
        # Our current threadpool has a max of 1 worker.
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()

        # Create the exchange if not already present
        self.exchange = "RMQ Labs"
        self.channel.exchange_declare(self.exchange)

        # Create the queue if not already present
        self.queue_name = "RMQ Lab Queue"
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(
            queue=self.queue_name,
            routing_key=self.routing_key,
            exchange=self.exchange,
        )
        self.channel.basic_consume(self.queue_name, self.on_message)

    def on_message(self, channel, method_frame, header_frame, body):
        print(
            f"Incoming Data. Method_Frame:{method_frame}\nHeader_Frame:{header_frame}\nBody:{body}"
        )
        if self.message_handler:
            self.message_handler(body)

        channel.basic_ack(method_frame.delivery_tag)

    def consume_block(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def start_consuming(self):
        self.pool.submit(self.consume_block)

    def stop_consuming(self):
        self.channel.channel.stop_consuming()
        print("Attempting to join consumer thread")
        self.pool.shutdown()


test_obj = MQConsumer("Test_Key")
test_obj.start_consuming()
time.sleep(300)
test_obj.stop_consuming()
