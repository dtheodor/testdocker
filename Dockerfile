FROM ubuntu:14.04

MAINTAINER Dimitris

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all python-pip libpq-dev python-dev

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./app.py /opt/app.py
WORKDIR /opt/

EXPOSE 5000
CMD ["python", "app.py"]
