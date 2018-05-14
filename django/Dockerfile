FROM python:3.6-stretch

ARG env
ENV ENV ${env:-dev}

ARG requirements_file
ENV REQUIREMENTS_FILE ${requirements_file:-base.txt}

ENV CLI_COLOR=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libcurl4-openssl-dev \
    libjpeg-dev \
    vim \
    ntp \
    python-dev \
    python3-dev \
    python-setuptools \
    python3-setuptools \
    software-properties-common \
    libpq-dev

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade wheel

RUN pip3 install \
    virtualenv \
    virtualenvwrapper

ENV WAITFORIT_VERSION="v1.3.1"
RUN curl -o /usr/local/bin/waitforit -sSL https://github.com/maxcnunes/waitforit/releases/download/$WAITFORIT_VERSION/waitforit-linux_amd64 && \
    chmod +x /usr/local/bin/waitforit

# Prevent Docker from re-running this layer unless we update requirements
ADD ./requirements/* /tmp/
WORKDIR /tmp
RUN pip3 install -r $REQUIREMENTS_FILE
WORKDIR /app

ADD . /app/


VOLUME /data
RUN chmod -R a+rw /data

# Add more columns to SSH terminal
RUN echo 'COLUMNS=140' >> ~/.bashrc