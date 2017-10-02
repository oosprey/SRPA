FROM python:3.5
MAINTAINER youchen <youchen.du@gmail.com>
USER root

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y mysql-client
RUN git clone https://github.com/Time1ess/SRPA
RUN pip install -r SRPA/requirements.txt

ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

EXPOSE 8000

ENV SRPA_SETTINGS production

CMD ["/SRPA/scripts/server/start.sh"]
