# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/

RUN mkdir /usr/src/media
RUN mkdir /usr/src/staticfiles

# set environment variables
# revents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
