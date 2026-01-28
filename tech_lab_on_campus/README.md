# Rabbit MQ On Campus Lab

## Background

The idea of this lab is to offer exposure to the RabbitMQ messaging framework, providing a basic understanding of the technology and the producer consumer relationship. During the lab you will apply your learning to create a small system to setup information updates on securities of interest.

## Lab Overview

This lab is structured as a progressive learning experience where you'll build your understanding of RabbitMQ through hands-on implementation:

### Lab Structure

**1. [Producer & Consumer](./producer_consumer/README.md)**

**2. [Topic Exchange](./topic_exchange/README.md)**

Each section builds upon the previous, introducing more sophisticated messaging patterns and real-world applications.

## Learning Outcomes

### Section 1: [Producer & Consumer](./producer_consumer/README.md)
- Understand the basic producer-consumer messaging pattern
- Implement a RabbitMQ producer class that publishes messages
- Implement a RabbitMQ consumer class that receives and processes messages
- Learn about direct exchanges and queue binding
- Practice collaborative development using Git workflows
- **Skills Gained**: Basic message queuing, asynchronous communication, Python OOP

### Section 2: [Topic Exchange](./topic_exchange/README.md)
- Main topic-based message routing using RabbitMQ topic exchanges
- Implement pattern-based message filtering with routing and binding keys
- Build a stock market update system with sector-based filtering
- **Skills Gained**: Advanced routing patterns, command-line argument parsing, real-world financial data messaging


## Key Technologies & Concepts

All necessary reference materials are provided in the [resources](./resources/) folder.
Throughout this lab, you'll work with:

**Python CS Concepts:**
- Classes & Object-Oriented Programming (OOP)
- Importing & Exporting Modules
- Inheritance and Interfaces

**RabbitMQ Concepts:**
- Producers and message publishing
- Consumers and message consumption
- Exchanges (Direct and Topic)
- Queues and message routing
- Binding keys and routing patterns

**Financial Concepts:**
- Stock tickers
- Industry sectors
- Market data updates

## Lab Instructions

### Step 0: Set Up Your Environment
Follow the [Setting Up Our Environment](#setting-up-our-environment) instructions below to:
- Fork and clone the repository
- Install Docker and Docker Compose
- Start the RabbitMQ container
- Verify your environment is working correctly

### Step 1: Complete Producer & Consumer Lab
Start with the [Producer & Consumer section](./producer_consumer/README.md) where you'll:
- Build your first RabbitMQ producer
- Build your first RabbitMQ consumer
- Test basic message passing
- Learn collaborative Git workflows

### Step 2: Complete Topic Exchange Lab
Continue to the [Topic Exchange section](./topic_exchange/README.md) where you'll:
- Implement topic-based routing
- Build a stock market messaging system
- Use pattern matching for message filtering
- Handle multiple consumers with different subscriptions

### Step 3: (Optional) Explore Stretch Goals
Each section includes stretch goals for advanced learning:
- Multiple topic subscriptions
- Complex routing patterns
- Real-time data streaming

## Setting Up Our Environment

### Option 1: Using GitHub Codespaces (Recommended)

GitHub Codespaces provides a cloud-based development environment that's ready to use with all dependencies pre-configured.

1. Navigate to [https://github.com/codespaces](https://github.com/codespaces)

2. Click on "New codespace" to create a new codespace for this repository.

3. Once your codespace is ready, open the terminal and navigate to the tech_lab_on_campus directory:
    ```sh
    cd tech_lab_on_campus
    ```

4. Start the Docker containers:
    ```sh
    docker-compose up
    ```

5. Once the containers are running, locate the **Ports** tab in your codespace (usually at the bottom of the screen).

6. Find port **15672** in the ports list and click on the globe icon or forwarded address beside it to open the RabbitMQ Management UI.

7. Log in to RabbitMQ using:
   - **Username:** rmq-docker-broker
   - **Password:** rmq-docker-broker

You are now ready to start the lab! Begin by navigating to the [producer_consumer](./producer_consumer/README.md) folder and reading the "README.md" file. Each of the units will contain a readme file which will give you the necessary instructions to complete the lab and test your solution.

### Option 2: Using Local Development Environment

For this project, we're going to leverage the use of Docker to create a helpful development environment for all of the engineers. [Docker](https://docs.docker.com/desktop/) is a tool used to integrate software dependencies and allow developers to quickly spin up software builds in portable lightweight containers which provide consistent environments, ensuring applications run the same way across various platforms.

1. Fork the repo
![fork](../data/Images/fork-1.JPG)

2. Clone the forked repo into your working directory. Copy ssh.
![ssh](../data/Images/copy_ssh.PNG)

    ```sh
    git clone [SSH KEY]
    ```

3. Navigate to the 'Tech-Lab-On-Campus' folder.
    ```sh
    cd learning_labs/Tech-Lab-On-Campus
    ```

4. Confirm that Docker and Docker Compose are working on your system.
    ```sh
    docker -v && docker-compose -v
    ```
* If this works correctly, you will have the versions of Docker and Docker Compose printed to the terminal.
* Note: If you encounter an error at this step navigate to advanced settings on your  Docker Desktop and ensure that `System (requires password)` is selected. This tab can be found by clicking on the gear icon in the top right corner.

5. Utilize Docker to generate and execute a functional image of the project directly from the terminal within your chosen Integrated Development Environment (IDE).

There are two options to work on this project. Option [A] using an IDE, we recommend using VSCode. Option [B] using the jupyter notebook. Follow the steps outlined for the desired option to ensure a smooth setup and execution process:

* A) IDE
    * In the terminal window of your IDE run:
        ```sh
        docker-compose up -d && docker-compose exec rmq_lab /bin/bash
        ```
        *  `docker-compose up -d` : Starts our rabbitmq and python service in detached mode (-d), running them in the background.
        * `docker-compose exec rmq_lab /bin/bash` : This command will open an interactive Bash shell inside the rmq_lab service container. Once you are inside the container you can run Python scripts.

        * Note: If you encounter an error such as `unix:///Users/userName/.docker/run/docker.sock. Is the docker daemon running?`, please ensure that your Docker application is running.

* B) Jupyter Notebook
    * In the terminal window of your IDE run:
        ```sh
        docker-compose up
        ```
    * In the output lines produced by the command, you will find three links providing access to the server hosting your Jupyter Notebook. Click on any one of these links to open and interact with the notebook. The links should resemble the following:
        ```
            rmq_lab-1   |     To access the server, open this file in a browser:
            rmq_lab-1   |         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-1-open.html
            rmq_lab-1   |     Or copy and paste one of these URLs:
            rmq_lab-1   |         http://d572024fabe2:8888/lab?token=4a07fca9cd4a66eba129533a6272f5f5443fdf3f0b7c0e5e
            rmq_lab-1   |         http://127.0.0.1:8888/lab?token=4a07fca9cd4a66eba129533a6272f5f5443fdf3f0b7c0e5e
        ```
6. Here are the steps to check that the environment is running correctly:
    * Log Into the RabbitMQ Website.
        * From your desktop, open Docker Desktop Dashboard.
        * Find the Rabbitmq container and click on the URL under Port(s) for the U.I. This should open up the RabbitMQ website on your default browser.
        * Login username and password should be "rmq-docker-broker"

    * Alternative:  Click on one of the generated URLs in your terminal, such as "http://localhost:30439/", once your docker container is up and running.

    * After setting up IDE you should have access to rabbit mq management. It will look like the following.
        ![rabbitmqup](../data/Images/rabbit_mq.PNG)
    * You are now ready to start the lab. Begin by navigating to the [producer_consumer](./producer_consumer/README.md) folder and reading the "README.md" file. Each of the units will contain a readme file which will give you the necessary instructions to complete the lab and test your solution.

## Troubleshooting

### Docker DNS Issue Fix
You might encounter an error while starting Docker up, most likely, while running the `python3.10 -m pip install -r requirements.txt` step. This error would be a DNS name resolution failure such as "Name or service not known" or "Temporary failure in name resolution". Follow the steps below to resolve the issue.

#### Mac
1. Clone the tech lab repo, then start up the container using `docker-compose up` to make sure it still fails
2. Uninstall Docker desktop: Open Docker Desktop -> Settings -> Click "bug" icon at the top right -> Uninstall Docker Desktop
3. In your terminal, run `brew uninstall docker --cask`
4. Run `brew list` to see if docker is still in the list. If so, force an uninstall with `brew uninstall --cask docker --force`
5. Run `ls /usr/local/bin/*docker*` to verify there are no results
6. Re-run the mac bootstrapper from https://bbgithub.dev.bloomberg.com/Local-Development/mac-universal-bootstrap
7. Bootstrapper will install the latest version of docker. Re-run the project

Refer to this doc for more detailed information on the fix: https://tutti.prod.bloomberg.com/local-development/troubleshooting/dns_issues#known-fix

#### Windows
1. Clone the tech lab repo, then start up the container using `docker-compose up`` to make sure it still fails
2. Run `sudo apt-get remove docker docker-engine docker.io containerd runc docker-ce docker-ce-cli` to remove docker from your system
3. Run `sudo rm -rf /var/lib/docker /etc/docker /etc/apparmor.d/docker /var/run/docker.sock /usr/local/bin/docker-compose /etc/docker` to delete remnants of Docker
4. Re-run the Windows bootstrapper from https://tutti.prod.bloomberg.com/windows-bootstrap/README
5. Bootstrapper will install the latest version of docker and wsl. Re-run the project in the latest wsl version

Refer to this doc for more detailed information on the fix: https://tutti.prod.bloomberg.com/local-development/troubleshooting/dns_issues#docker-containers-in-wsl



