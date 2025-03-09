def get_mock_jobs():
    return [
        {
            "id": "job_1",
            "connectionId": "Salesforce",
            "status": "failed",
            "duration": 120,
            "recordsSynced": 1500
        },
        {
            "id": "job_2",
            "connectionId": "Snowflake",
            "status": "running",
            "duration": 240,
            "recordsSynced": 8500
        }
    ]

def get_mock_logs(job_id):
    return f"""2024-05-20 ERROR: Connection timeout
2024-05-20 WARN: API rate limit exceeded
2024-05-20 INFO: Retrying (3/5)
2024-05-20 ERROR: Failed to authenticate"""