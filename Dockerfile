FROM python:3.6-slim

LABEL maintainer='biggstd@gmail.com'

RUN apt-get update

RUN mkdir /opt/pynome && mkdir /pynome

# Copy the pynome dir.
COPY . /opt/pynome/

# Install Pynome requirements.
RUN python -m pip install -r /opt/pynome/requirements.txt

# Copy the config file to the image.
COPY pynome_config.json /pynome/pynome_config.json

WORKDIR /opt/pynome/
# Install Pynome.
RUN python /opt/pynome/setup.py install

WORKDIR /pynome/

CMD ["pynome", "discover", "list"]
