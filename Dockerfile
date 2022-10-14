FROM python:3.8
ENV DockerHOME=/home/app/webapp

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

RUN pip install --upgrade pip

COPY . $DockerHOME

RUN pip install -r requirements.txt
