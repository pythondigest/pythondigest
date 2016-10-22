FROM python:3.5.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /pythondigest
WORKDIR /pythondigest
COPY requirements.txt /pythondigest/
RUN pip install -r requirements.txt
ADD . /pythondigest/
EXPOSE 8099
