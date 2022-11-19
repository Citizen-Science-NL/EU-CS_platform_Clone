# Set base image (host OS)
FROM python:3.9-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# By default, listen on port 8000
EXPOSE 80
EXPOSE 8000

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get install -y libgdal-dev

RUN pip3 install GDAL==3.2.2.1
# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
