# Set base image (host OS)
# The Django version we are using depends on Sequence which was moved in python 3.10. That's why we install 3.9. 
FROM python:3.9-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# By default, listen on port 8000
EXPOSE 80
EXPOSE 8000

# Installing GDAL --> this is a dependancy not obtainable through PIP
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Set the working directory in the container
WORKDIR /src

# Specify the command to run on container start
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
#CMD [ "gunicorn", "eucs_platform.wsgi" ]
