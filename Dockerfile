# Use a prepared image with python 3.6.
FROM python:3.6-slim

# Dockerfile information.
LABEL maintainer='biggstd@gmail.com'


# Update package manager and install basics.
RUN apt-get update \
  && apt-get -y install git wget unzip build-essential


# Install IRODs
RUN apt-get -y install libfuse2 expect jq tree \
  && wget ftp://ftp.renci.org/pub/irods/releases/4.1.11/ubuntu14/irods-icommands-4.1.11-ubuntu14-x86_64.deb \
  && dpkg -i irods-icommands-4.1.11-ubuntu14-x86_64.deb \
  && chmod 755 /usr/local/share/*


# Install hisat2
RUN wget -q ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-Linux_x86_64.zip \
  && unzip hisat2-2.1.0-Linux_x86_64.zip \
  && mv hisat2-2.1.0 /opt/hisat2
ENV PATH="/opt/hisat2:$PATH"

# Install Cufflinks
RUN wget -q http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz \
  && tar -xzf cufflinks-2.2.1.Linux_x86_64.tar.gz \
  && mv cufflinks-2.2.1.Linux_x86_64 /opt/cufflinks
ENV PATH="/opt/cufflinks:$PATH"


# Install gffread
WORKDIR /opt
RUN git clone https://github.com/gpertea/gclib \
  && git clone https://github.com/gpertea/gffread
WORKDIR /opt/gffread
RUN make
ENV PATH="/opt/gffread:$PATH"

# set user/group IDs for irods account
RUN groupadd -r irods --gid=998 \
    && useradd -r -g irods -d /var/lib/irods --uid=998 irods


# grab gosu for easy step-down from root
ENV GOSU_VERSION 1.10
RUN set -x \
    && apt-get update && apt-get install -y --no-install-recommends ca-certificates wget && rm -rf /var/lib/apt/lists/* \
    && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" \
    && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
    && rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu \
    && gosu nobody true \
    && apt-get purge -y --auto-remove wget

# default iRODS env
ENV IRODS_PORT=1247
ENV IRODS_PORT_RANGE_BEGIN=20000
ENV IRODS_PORT_RANGE_END=20199
ENV IRODS_CONTROL_PLANE_PORT=1248
# iinit parameters
ENV IRODS_HOST=scidas-irods.cahnrs.wsu.edu
ENV IRODS_USER_NAME=biggst
ENV IRODS_ZONE_NAME=scidasZone
ENV IRODS_CWD=/ScidasZone/Sysbio/testgenomes
# TODO: remove pw -- convert to docker secret.
ENV IRODS_PASSWORD=3t5fpQLVynUw
# UID / GID settings
ENV UID_IRODS=998
ENV GID_IRODS=998

EXPOSE $IRODS_PORT $IRODS_CONTROL_PLANE_PORT $IRODS_PORT_RANGE_BEGIN-$IRODS_PORT_RANGE_END

COPY /scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
# RUN /docker-entrypoint.sh
COPY . /tmp
RUN cp /tmp/scripts/docker-entrypoint.sh /docker-entrypoint.sh \
    && rm -rf /tmp/*


# Create the diectories for pynome.
RUN mkdir /opt/pynome \
  && mkdir /pynome
VOLUME /pynome

# Copy the pynome dir.
COPY . /opt/pynome/

# Install Pynome requirements.
RUN python -m pip install -r /opt/pynome/requirements.txt

# Change the working directory -- required for the install.py to function.
WORKDIR /opt/pynome

# Install Pynome.
RUN python /opt/pynome/setup.py install

# Set the default command to be launched for this container.
WORKDIR /pynome

# Disable SSL verification...
ENV PYTHONHTTPSVERIFY=0

ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["ls", "-lsa"]
CMD ["pynome", "--config=/opt/pynome/pynome_config.json", "discover", "download", "sra", "prepare", "putirods"]
