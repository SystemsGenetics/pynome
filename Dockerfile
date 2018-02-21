FROM python:3.6-slim

LABEL maintainer='biggstd@gmail.com'

RUN apt-get update
# RUN apt-get install -y software-properties-common vim
# RUN add-apt-repository ppa:jonathonf/python-3.6
# RUN apt-get update

# RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
# RUN python3.6 -m pip install pip --upgrade
# RUN python3.6 -m pip install wheel


RUN mkdir /opt/pynome
RUN mkdir /pynome

# Copy the pynome dir.
COPY . /opt/pynome/

# Install Pynome requirements.
RUN python3.6 -m pip install -r /opt/pynome/requirements.txt

# Install Pynome.
RUN python3.6 /opt/pynome/setup.py install

# Copy the config file to the image.
COPY pynome_config.json /pynome/pynome_config.json

WORKDIR /pynome

CMD ["pynome", "--help"]
