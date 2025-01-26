# Configuration Files

## Overview
The agent is configured using YAML files, which define what data to collect, which integrations to enable, and how to communicate with the CloudPioneer backend.

## Example Configuration File Snippet
```yaml
logs_enabled: true
apm_config:
  enabled: true
network_config:
  enabled: true
```

## Tags
Tags can be applied to metrics, logs, and traces to group and filter data for analysis (e.g., environment:production, region:us-east-1).
