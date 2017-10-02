FROM python:3.5
MAINTAINER youchen <youchen.du@gmail.com>
USER root

RUN git clone https://github.com/Time1ess/SRPA
RUN mkdir /SRPA/media
RUN pip install -r SRPA/requirements.txt

ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENV SRPA_SETTINGS production
ENTRYPOINT ["/entrypoint.sh"]
