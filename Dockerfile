FROM python:3.12

RUN mkdir /opt/desigo-scraper
WORKDIR /opt/desigo-scraper

RUN apt-get update \
  && apt-get install -y cron \
  && rm -rf /var/lib/apt/lists/* /var/log/* /tmp/* /root/.cache

COPY requirements.txt /opt/desigo-scraper/requirements.txt
RUN pip install -r requirements.txt

COPY / /opt/desigo-scraper

CMD /opt/desigo-scraper/run
