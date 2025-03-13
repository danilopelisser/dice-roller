import logging
from flask import Flask, jsonify
import os
from random import randint
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Configurar logging para Loki
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar handler para enviar logs ao Loki
try:
    from logging_loki import LokiHandler
    loki_handler = LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
        tags={"application": "dice-roller"},
        version="1"
    )
    logger.addHandler(loki_handler)
    logger.info("Loki handler initialized successfully")
except ImportError:
    logger.warning("python-logging-loki not installed. Install with: pip install python-logging-loki")
except Exception as e:
    logger.error(f"Failed to initialize Loki handler: {str(e)}")

# Configurar o recurso com o nome do serviço
resource = Resource(attributes={
    SERVICE_NAME: "dice-roller"
})

# Configurar o provedor de traces (mantido para traces, mas focaremos em logs)
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="tempo:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
metrics = PrometheusMetrics(app)

@app.route('/', methods=['GET'])
def roll_dice():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("roll_dice_operation") as span:
        dice_value = randint(1, 6)
        logger.info(f"Dice rolled: {dice_value}, Span ID: {span.get_span_context().span_id}")
        return jsonify({'dice_value': dice_value})

@app.route("/fail")
def fail():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("fail_operation") as span:
        logger.info(f"Starting fail operation, Span ID: {span.get_span_context().span_id}")
        try:
            1/0
        except Exception as e:
            logger.error(f"Failed operation: {str(e)}")
            raise
    return 'fail'

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
