# DevOps Monitoring Agent

The DevOps Monitoring Agent collects infrastructure metrics
and sends them to the FastAPI backend.

## Collected Metrics

- CPU utilization
- Memory utilization
- Disk utilization
- Process count
- Network bytes sent
- Network bytes received
- Hostname
- IP address
- Operating system
- CPU cores
- Total memory

## Configuration

Environment variables:

```env
BACKEND_URL=http://backend:8000
AGENT_INTERVAL=30
AGENT_USERNAME=agent
AGENT_PASSWORD=Agent@123
REQUEST_TIMEOUT=10