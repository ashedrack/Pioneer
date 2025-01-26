import time
from typing import Any, Dict, List

import mysql.connector

from ..agent import BaseCollector, Metric


class MySQLCollector(BaseCollector):
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(agent_config)
        self.db_config = agent_config.get("mysql", {})
        self._setup_connection()

    def _setup_connection(self):
        self.connection = mysql.connector.connect(
            host=self.db_config.get("host", "localhost"),
            user=self.db_config.get("user"),
            password=self.db_config.get("password"),
            database=self.db_config.get("database"),
        )

    def collect(self) -> List[Metric]:
        metrics = []
        timestamp = time.time()

        try:
            if not self.connection.is_connected():
                self._setup_connection()

            cursor = self.connection.cursor()

            # Collect global status metrics
            cursor.execute("SHOW GLOBAL STATUS")
            status_metrics = cursor.fetchall()

            important_metrics = {
                "Queries": "mysql.queries",
                "Threads_connected": "mysql.threads.connected",
                "Threads_running": "mysql.threads.running",
                "Slow_queries": "mysql.queries.slow",
                "Questions": "mysql.questions",
                "Com_select": "mysql.commands.select",
                "Com_insert": "mysql.commands.insert",
                "Com_update": "mysql.commands.update",
                "Com_delete": "mysql.commands.delete",
            }

            for row in status_metrics:
                var_name, value = row
                if var_name in important_metrics:
                    try:
                        metric_value = float(value)
                        metrics.append(
                            Metric(
                                name=important_metrics[var_name],
                                value=metric_value,
                                tags={
                                    "host": self.db_config.get("host", "localhost"),
                                    "database": self.db_config.get(
                                        "database", "unknown"
                                    ),
                                },
                                timestamp=timestamp,
                                source="mysql",
                            )
                        )
                    except (ValueError, TypeError):
                        self.logger.warning(
                            f"Could not convert {var_name} value to float: {value}"
                        )

            # Collect InnoDB metrics
            cursor.execute("SHOW ENGINE INNODB STATUS")
            innodb_status = cursor.fetchone()[2]

            # Parse InnoDB metrics (simplified)
            metrics.extend(self._parse_innodb_metrics(innodb_status, timestamp))

            cursor.close()

        except Exception as e:
            self.logger.error(f"Error collecting MySQL metrics: {e}")

        return metrics

    def _parse_innodb_metrics(self, status: str, timestamp: float) -> List[Metric]:
        metrics = []
        try:
            # Extract basic InnoDB metrics
            if "transactions" in status.lower():
                metrics.append(
                    Metric(
                        name="mysql.innodb.transactions",
                        value=1.0,  # Placeholder value
                        tags={
                            "host": self.db_config.get("host", "localhost"),
                            "database": self.db_config.get("database", "unknown"),
                        },
                        timestamp=timestamp,
                        source="mysql",
                    )
                )
        except Exception as e:
            self.logger.error(f"Error parsing InnoDB metrics: {e}")

        return metrics
