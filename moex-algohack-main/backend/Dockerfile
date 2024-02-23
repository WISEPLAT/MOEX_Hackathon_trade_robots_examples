# Use the official Python image from Docker Hub
FROM python:3.10

# Prevent Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevent Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker container
WORKDIR /code

# Install the psycopg2 dependency
RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && pip install django moexalgo pandas

# Copy the project files into the working directory
COPY . /code/

# Expose the port the app runs on
EXPOSE 8000

# Run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
