# Use the official Jupyter Notebook Image as the base image
FROM artprod.dev.bloomberg.com/pre-devx/minimal-bbg-notebook:3.10

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Set envrionmental variables for python module
ENV PYTHONPATH /app/consumer:/app/producer:/app/market_watch

# Default command to be run once container starts
ENTRYPOINT ["/bin/bash","-c","jupyter lab"]
