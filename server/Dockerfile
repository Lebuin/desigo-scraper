FROM python:3.12

RUN mkdir /opt/server
WORKDIR /opt/server

EXPOSE 5000

COPY requirements.txt /opt/server/requirements.txt
RUN pip install -r requirements.txt

COPY / /opt/server

CMD /opt/server/run
