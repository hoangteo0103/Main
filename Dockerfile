FROM ubuntu:14.04

RUN apt-get update
RUN apt-get -y install firefox

CMD ["firefox"]