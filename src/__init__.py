from flask import Flask
from src.api.resource_metrics import resource_metrics_bp
from src.api.logs import logs_bp
from src.api.process_monitoring import process_monitoring_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(resource_metrics_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(process_monitoring_bp)
