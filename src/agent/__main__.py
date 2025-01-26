import argparse
import logging
import os
import sys

from .agent import MonitoringAgent
from .backends.aws import AWSBackend
from .backends.azure import AzureBackend
from .backends.gcp import GCPBackend
from .collectors.docker import DockerCollector
from .collectors.mysql import MySQLCollector
from .collectors.system import SystemMetricsCollector


def setup_logging(level):
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main():
    parser = argparse.ArgumentParser(description="Cloud Pioneer Monitoring Agent")
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to configuration file"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    args = parser.parse_args()
    setup_logging(args.log_level)

    try:
        agent = MonitoringAgent(args.config)

        # Register collectors based on configuration
        if agent.config["collectors"]["system"]["enabled"]:
            agent.register_collector("system", SystemMetricsCollector(agent.config))

        if agent.config["collectors"]["mysql"]["enabled"]:
            agent.register_collector("mysql", MySQLCollector(agent.config))

        if agent.config["collectors"]["docker"]["enabled"]:
            agent.register_collector("docker", DockerCollector(agent.config))

        # Register backends
        if agent.config["backends"]["aws"]["enabled"]:
            agent.register_backend("aws", AWSBackend(agent.config["backends"]["aws"]))

        if agent.config["backends"]["azure"]["enabled"]:
            agent.register_backend(
                "azure", AzureBackend(agent.config["backends"]["azure"])
            )

        if agent.config["backends"]["gcp"]["enabled"]:
            agent.register_backend("gcp", GCPBackend(agent.config["backends"]["gcp"]))

        # Start the agent
        agent.start()

        # Keep the main thread alive
        try:
            while True:
                import time

                time.sleep(1)
        except KeyboardInterrupt:
            agent.stop()

    except Exception as e:
        logging.error(f"Failed to start agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
