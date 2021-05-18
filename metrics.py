import sys
import time

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter
from opentelemetry.sdk.metrics.export.controller import PushController
from prometheus_client import start_http_server

# Start Prometheus client
start_http_server(port=8000, addr="localhost")

batcher_mode = "stateful"
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__, batcher_mode == "stateful")
#exporter = ConsoleMetricsExporter()
exporter = PrometheusMetricsExporter("MyAppPrefix")
controller = PushController(meter, exporter, 5)

requests_counter = meter.create_counter(
    name="requests",
    description="number of requests",
    unit="1",
    value_type=int
)

requests_counter.add(25, {"environment": "staging"})
time.sleep(5)

requests_counter.add(20, {"environment": "staging"})
time.sleep(10)

# this line is added to keep the http server up long
# enough to scrape.
input("Press any key to exit...")