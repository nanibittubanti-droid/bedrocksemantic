import logging
from typing import Optional

from app.config import Config

try:
    from opentelemetry import metrics, trace
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
except ImportError:  # pragma: no cover
    metrics = None
    trace = None
    OTLPMetricExporter = None
    OTLPSpanExporter = None
    MeterProvider = None
    ConsoleMetricExporter = None
    PeriodicExportingMetricReader = None
    Resource = None
    SERVICE_NAME = None
    TracerProvider = None
    BatchSpanProcessor = None
    ConsoleSpanExporter = None

tracer = None


class NoOpSpan:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class NoOpTracer:
    def start_as_current_span(self, name: str, attributes: dict | None = None):
        return NoOpSpan()


class NoOpCounter:
    def add(self, amount: int = 1, attributes: dict | None = None):
        pass


def _make_resource(config: Config):
    if Resource is None:
        return None
    return Resource.create(
        {
            SERVICE_NAME: config.otel_service_name,
            "deployment.environment": config.otel_environment,
        }
    )


def _create_span_exporter(endpoint: Optional[str]):
    if OTLPSpanExporter is None or ConsoleSpanExporter is None:
        return None
    if endpoint:
        logging.getLogger(__name__).info("Configuring OTLP span exporter endpoint=%s", endpoint)
        return OTLPSpanExporter(endpoint=endpoint)
    logging.getLogger(__name__).info("Configuring console span exporter")
    return ConsoleSpanExporter()


def _create_metric_exporter(endpoint: Optional[str]):
    if OTLPMetricExporter is None or ConsoleMetricExporter is None:
        return None
    if endpoint:
        logging.getLogger(__name__).info("Configuring OTLP metric exporter endpoint=%s", endpoint)
        return OTLPMetricExporter(endpoint=endpoint)
    logging.getLogger(__name__).info("Configuring console metric exporter")
    return ConsoleMetricExporter()


def configure_observability(config: Config):
    global tracer
    if trace is None or metrics is None or TracerProvider is None or MeterProvider is None:
        logging.getLogger(__name__).warning(
            "OpenTelemetry packages are not installed; using no-op observability implementation"
        )
        tracer = NoOpTracer()
        return tracer, NoOpCounter(), NoOpCounter()

    resource = _make_resource(config)

    tracer_provider = TracerProvider(resource=resource)
    span_exporter = _create_span_exporter(config.otel_exporter_endpoint)
    if span_exporter is not None:
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)
    current_tracer = trace.get_tracer(config.otel_service_name)

    metric_exporter = _create_metric_exporter(config.otel_exporter_endpoint)
    metric_readers = []
    if metric_exporter is not None:
        metric_readers.append(PeriodicExportingMetricReader(metric_exporter))
    meter_provider = MeterProvider(resource=resource, metric_readers=metric_readers)
    metrics.set_meter_provider(meter_provider)

    meter = metrics.get_meter(config.otel_service_name, version="0.1.0")
    assessment_counter = meter.create_counter(
        "assessment_runs",
        description="Number of completed assessment runs",
        unit="1",
    )
    error_counter = meter.create_counter(
        "assessment_errors",
        description="Number of failed assessments",
        unit="1",
    )

    tracer = current_tracer
    return current_tracer, assessment_counter, error_counter
