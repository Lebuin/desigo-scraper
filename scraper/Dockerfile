FROM python:3.12-slim

RUN mkdir /opt/scraper
WORKDIR /opt/scraper

RUN apt-get update \
  && apt-get install -y cron wget \
  && rm -rf /var/lib/apt/lists/* /var/log/* /tmp/* /root/.cache

COPY requirements.txt /opt/scraper/requirements.txt
RUN pip install -r requirements.txt

COPY / /opt/scraper

CMD /opt/scraper/run
