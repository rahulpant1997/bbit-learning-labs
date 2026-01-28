FROM artprod.dev.bloomberg.com/pre-devx/minimal-bbg-notebook:3.10
WORKDIR /app
COPY requirements.txt .
RUN python3.10 -m pip install -r requirements.txt
ENV PYTHONPATH /app/consumer:/app/producer:/app/market_watch

ENTRYPOINT ["/bin/bash", "-c", "jupyter lab"]
