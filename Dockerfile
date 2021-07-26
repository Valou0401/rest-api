FROM python

#install pip
RUN apt-get update && apt-get install -y python3-pip
#install requests
RUN python3 -m pip install requests

RUN /opt/local/remote

COPY sources/remote.py /opt/local/remote/remote.py
COPY sources/remote.sh /opt/local/remote/remote.sh

ENV PATH /opt/local/remote:$PATH
ENTRYPOINT ["/bin/bash", "remote.sh"]
