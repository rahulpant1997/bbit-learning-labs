# Problem Defintion: ✨Consumer✨

##  Instructions
Create a .py file that will contain a class that is setup to be a consumer in the RabbitMQ framework. This class will inherit from the mqConsumerInterface and consume and print a simple UTF-8 string message. 

Below are bullet points of the criteria:
- Your class should be named mqConsumer.
- Your class should inherit from our mqConsumerInterface.
- The class name should be `mqConsumer` & the source file should be called `consumer_sol.py`
- Constructor: Save the three variables needed to instantiate the class.
- Constructor: Call the setupRMQConnection function.
- setupRMQConnection Function: Establish connection to the RabbitMQ service, declare a queue and exchange, bind the binding key to the queue on the exchange and finally set up a callback function for receiving messages
- onMessageCallback: Print the UTF-8 string message and then close the connection.
- startConsuming:  Consumer should start listening for messages from the queue.

###### [Note: Utilize the following resource to help instantiate the Producer Class: [RabbitMQ Tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)]

## Testing
In order to verify that the consumer class was properly we'll use the provider publisher file. Follow the below instructions
1. Run the publish.py file using the python interpreter. This will publish a message using RabbitMQ
* For this we'll be importing the solution of your publisher from the first unit. If you name either the producer class or file a different value from the expectation you will need to modify the import in `publish.py` file.
2. Run the consumer.py file using the python interpreter. This file will import you newly created class `mqConsumer` from `consumer_sol.py`. "Hello World" should now be displayed on your terminal if you instantiate & implemented the consumer class correctly.
