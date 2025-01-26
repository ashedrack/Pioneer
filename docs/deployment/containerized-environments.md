# Use in Containerized Environments

## Docker
The agent runs as a container and monitors other containers on the same host by mounting the Docker socket.

## Kubernetes
- The agent is deployed as a DaemonSet, ensuring a single agent runs on every node in the cluster.
- It integrates with Kubernetes APIs to collect metrics and logs from pods, nodes, and cluster resources.
