# Use an appropriate base image for Python, adjust version as needed
FROM python:3.12

# Set environment variables to prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entire project to the working directory in the container
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run any additional setup commands (if necessary)
# For example, migrate database schema
RUN python manage.py migrate

# Specify the command to run your Django application with Gunicorn
CMD ["gunicorn", "ats_project.wsgi:application", "--bind", "0.0.0.0:8000"]
