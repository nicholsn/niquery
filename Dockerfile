# Full build in a single container
FROM ubuntu:12.04
MAINTAINER Nolan Nichols <nolan.nichols@gmail.com>

RUN apt-get update 
RUN apt-get install -y python-software-properties git
RUN add-apt-repository -y ppa:rquillo/ansible
RUN apt-get update && apt-get upgrade
RUN apt-get install -y ansible
RUN ansible-pull -C master -d /opt -i provisioning/hosts -U https://github.com/niquery/niquery.git provisioning/local.yml
