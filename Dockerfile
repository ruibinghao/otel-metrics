FROM python:3.8-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

COPY requirements requirements
COPY opentelemetry-python opentelemetry-python

RUN pip install -U setuptools
RUN pip install -e ./opentelemetry-python/opentelemetry-api
RUN pip install -e ./opentelemetry-python/opentelemetry-sdk
RUN pip install -e ./opentelemetry-python/opentelemetry-instrumentation
RUN pip install -e ./opentelemetry-python/exporter/opentelemetry-exporter-prometheus
RUN pip install -e ./opentelemetry-python/exporter/opentelemetry-exporter-jaeger
RUN pip install -r requirements/common.txt

COPY tracing-metrics-flask.py boot-flask-slim.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot-flask.sh"]
