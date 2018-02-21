FROM ubuntu:16.04

LABEL maintainer='biggstd@gmail.com'

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

# Install Pynome's requirements.
RUN python3.6 -m pip install -r requirements.txt

RUN mkdir /opt/pynome

# Copy the pynome dir.
COPY . /opt/pynome/

# Install Pynome.
RUN python3.6 /opt/pynome/setup.py

# Copy the config file to the image.
COPY /pynome/

WORKDIR /pynome

CMD ["pynome"]
