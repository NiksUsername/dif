FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install git
RUN apt-get update && apt-get install -y git

# Install dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Change the working directory to where manage.py is
WORKDIR /app

# Expose the port Django runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]