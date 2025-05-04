# Base image
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock first (for better cache use)
COPY Pipfile* ./

# Tell pipenv to use the current system Python
ENV PIPENV_PYTHON=/usr/local/bin/python

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the backend source code
COPY . .

# Expose the backend port
EXPOSE 8000

# Set PYTHONPATH to recognize `src` as root
ENV PYTHONPATH=src

# Run the app
CMD ["pipenv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
