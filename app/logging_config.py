import logging

try:
    from opentelemetry import trace
except ImportError:  # pragma: no cover
    trace = None

try:
    from pythonjsonlogger import jsonlogger
except ImportError:  # pragma: no cover
    jsonlogger = None


def _format_trace_id(trace_id: int) -> str:
    return format(trace_id, "032x") if trace_id else ""


def _format_span_id(span_id: int) -> str:
    return format(span_id, "016x") if span_id else ""


class TraceContextFilter(logging.Filter):
    def __init__(self, service_name: str, environment: str) -> None:
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def filter(self, record: logging.LogRecord) -> bool:
        if trace is not None:
            span = trace.get_current_span()
            span_context = span.get_span_context()
            record.trace_id = _format_trace_id(span_context.trace_id) if span_context.is_valid else ""
            record.span_id = _format_span_id(span_context.span_id) if span_context.is_valid else ""
        else:
            record.trace_id = ""
            record.span_id = ""

        record.service_name = self.service_name
        record.environment = self.environment
        return True


def configure_logging(
    level: str = "INFO",
    log_format: str = "plain",
    service_name: str = "waf-assessment-platform",
    environment: str = "production",
) -> None:
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    handler = logging.StreamHandler()
    if log_format == "json" and jsonlogger is not None:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s %(service_name)s %(environment)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s [trace_id=%(trace_id)s span_id=%(span_id)s service_name=%(service_name)s environment=%(environment)s]"
        )
    handler.setFormatter(formatter)
    handler.addFilter(TraceContextFilter(service_name, environment))

    root_logger.addHandler(handler)
    logging.captureWarnings(True)
