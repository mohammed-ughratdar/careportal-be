# Use an official Python image as base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the entire backend project (one level up)
COPY app /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Expose the FastAPI port
EXPOSE 8000

# Move one directory up and run the app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
