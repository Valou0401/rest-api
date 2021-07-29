FROM python 

#install pip
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get install -y vim
#install requests
RUN python3 -m pip install requests
RUN python3 -m pip install python-jenkins

RUN mkdir remote

COPY sources/remote.py sources/remote.py
COPY sources/remote.sh sources/remote.sh
COPY sources/config sources/config
COPY sources/xml_config sources/xml_config

EXPOSE 8080
EXPOSE 80

ENV PATH remote:$PATH
#ENTRYPOINT ["/bin/bash", "remote.sh"]
