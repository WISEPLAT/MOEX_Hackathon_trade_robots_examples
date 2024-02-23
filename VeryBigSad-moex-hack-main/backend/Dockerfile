FROM python:3.11.6-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.2.2

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy the `pyproject.toml` and optionally the `poetry.lock` file
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the application code to the container
COPY ./app /app

# Copy your entrypoint script
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

# Use the entrypoint script to run the application
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
