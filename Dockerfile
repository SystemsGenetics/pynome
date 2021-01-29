FROM ubuntu:20.04


################## METADATA ######################
LABEL base_image="ubuntu:20.04"
LABEL software="Pynome Image"
LABEL software.version="1.0.0"
LABEL about.summary="Docker image for Pynome"
LABEL about.home=""
LABEL about.documentation=""
LABEL about.license_file=""


################## MAINTAINER ######################
MAINTAINER Josh Burns <4ctrl.alt.del@gmail.com>


# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND noninteractive


# Update and install basic packages
RUN apt-get update -qq \
  && apt-get install -qq -y wget unzip python python3 python3-pip


# Copy this repository and install pynome
COPY . /tmp/pynome
RUN cd /tmp/pynome \
  && pip3 install . \
  && cd .. \
  && rm -fr pynome


# Install hisat2 version 2.1.0
RUN wget -q ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-Linux_x86_64.zip \
  && unzip -q hisat2-2.1.0-Linux_x86_64.zip \
  && mv hisat2-2.1.0 /usr/local \
  && rm hisat2-2.1.0-Linux_x86_64.zip
ENV PATH "$PATH:/usr/local/hisat2-2.1.0"


# Install kallisto verison 0.45.0
RUN wget -q https://github.com/pachterlab/kallisto/releases/download/v0.45.0/kallisto_linux-v0.45.0.tar.gz \
  && tar -xf kallisto_linux-v0.45.0.tar.gz  \
  && mv kallisto_linux-v0.45.0 /usr/local/kallisto-0.45.0 \
  && chmod 755 /usr/local/kallisto-0.45.0/kallisto \
  && ln -sfn /usr/local/kallisto-0.45.0/kallisto /usr/bin/kallisto \
  && rm kallisto_linux-v0.45.0.tar.gz


# Install salmon verison 0.12.0
RUN wget -q https://github.com/COMBINE-lab/salmon/releases/download/v0.12.0/salmon-0.12.0_linux_x86_64.tar.gz \
  && tar -xf salmon-0.12.0_linux_x86_64.tar.gz \
  && mv salmon-0.12.0_linux_x86_64 /usr/local/salmon-0.12.0 \
  && chmod 755 /usr/local/salmon-0.12.0/bin/salmon \
  && ln -sfn /usr/local/salmon-0.12.0/bin/salmon /usr/bin/salmon \
  && rm salmon-0.12.0_linux_x86_64.tar.gz


# Install gffread version 0.12.2
RUN wget -q http://ccb.jhu.edu/software/stringtie/dl/gffread-0.12.2.Linux_x86_64.tar.gz \
  && tar -xf gffread-0.12.2.Linux_x86_64.tar.gz \
  && cp gffread-0.12.2.Linux_x86_64/gffread /usr/bin/gffread \
  && rm -fr gffread-0.12.2.Linux_x86_64 gffread-0.12.2.Linux_x86_64.tar.gz
