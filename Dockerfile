FROM python:3
MAINTAINER Ameya Lokare <lokare.ameya@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN apt-get -qy update && apt-get -qy install python3-pip && pip3 install pipenv
RUN pip install pipenv

RUN mkdir -p /opt/services/flaskapp/src

#VOLUME ["/opt/services/flaskapp/src"]
# We copy the requirements.txt file first to avoid cache invalidations

COPY Pipfile* /opt/services/flaskapp/src/
#COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src

RUN pipenv install --system

#RUN pip install -r requirements.txt
COPY . /opt/services/flaskapp/src
RUN python3 setup.py install

EXPOSE 5090
CMD ["python", "app.py"]
