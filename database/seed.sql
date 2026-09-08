INSERT INTO servers (
    hostname,
    ip_address,
    environment,
    operating_system,
    status,
    cpu_cores,
    memory_total_mb,
    description
)
VALUES
(
    'monitoring-server',
    '10.0.1.10',
    'development',
    'Ubuntu Linux',
    'online',
    2,
    4096,
    'Main monitoring server'
),
(
    'application-server',
    '10.0.2.10',
    'development',
    'Ubuntu Linux',
    'online',
    2,
    4096,
    'Application server'
)
ON CONFLICT (hostname) DO NOTHING;


INSERT INTO applications (
    name,
    server_id,
    version,
    port,
    status
)
SELECT
    'Monitoring API',
    id,
    '1.0.0',
    8000,
    'running'
FROM servers
WHERE hostname = 'monitoring-server';


INSERT INTO applications (
    name,
    server_id,
    version,
    port,
    status
)
SELECT
    'Sample Web Application',
    id,
    '1.0.0',
    8080,
    'running'
FROM servers
WHERE hostname = 'application-server';