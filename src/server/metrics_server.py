import time
from typing import Any, Dict, List

import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer
from influxdb_client import InfluxDBClient
from pydantic import BaseModel

from ..analysis.trend_analyzer import TrendAnalyzer

app = FastAPI(title="Cloud Pioneer Metrics Server")
security = HTTPBearer()


class MetricData(BaseModel):
    name: str
    value: float
    tags: Dict[str, str]
    timestamp: float
    source: str


class MetricsPayload(BaseModel):
    metrics: List[MetricData]
    agent_id: str


class AnalysisRequest(BaseModel):
    resource_id: str
    metric_name: str
    days: int = 30


class MetricsServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.influx_client = InfluxDBClient(
            url=config["influxdb"]["url"],
            token=config["influxdb"]["token"],
            org=config["influxdb"]["org"],
        )
        self.write_api = self.influx_client.write_api()
        self.trend_analyzer = TrendAnalyzer(config["influxdb"])

    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.config["jwt_secret"], algorithms=["HS256"])
            return True
        except:
            return False

    async def store_metrics(self, metrics: List[MetricData], agent_id: str):
        points = []
        for metric in metrics:
            point = {
                "measurement": metric.name,
                "tags": {**metric.tags, "agent_id": agent_id},
                "fields": {"value": metric.value},
                "time": int(metric.timestamp * 1e9),
            }
            points.append(point)

        try:
            self.write_api.write(
                bucket=self.config["influxdb"]["bucket"], record=points
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_analysis(
        self, resource_id: str, metric_name: str, days: int
    ) -> Dict[str, Any]:
        try:
            return self.trend_analyzer.analyze_resource_patterns(
                resource_id=resource_id, metric_name=metric_name, days=days
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Initialize server with configuration
server_config = {
    "influxdb": {
        "url": "http://localhost:8086",
        "token": "your-token",
        "org": "your-org",
        "bucket": "metrics",
    },
    "jwt_secret": "your-secret-key",
}

metrics_server = MetricsServer(server_config)


@app.post("/metrics")
async def receive_metrics(
    payload: MetricsPayload, token: HTTPBearer = Security(security)
):
    if not metrics_server.verify_token(token.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")

    await metrics_server.store_metrics(payload.metrics, payload.agent_id)
    return {"status": "success"}


@app.get("/analysis")
async def get_analysis(
    request: AnalysisRequest, token: HTTPBearer = Security(security)
):
    if not metrics_server.verify_token(token.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")

    return await metrics_server.get_analysis(
        request.resource_id, request.metric_name, request.days
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
