FROM artprod.dev.bloomberg.com/pre-devx/minimal-bbg-notebook:3.10

WORKDIR /app
COPY requirements.txt .
COPY requirements-dev.txt .
COPY pyproject.toml .
RUN python3.10 -m pip install -r requirements.txt
RUN python3.10 -m pip install -r requirements-dev.txt
ENV PYTHONPATH /app/portfolio_manager

ENTRYPOINT ["/bin/bash", "-c", "jupyter lab"]


