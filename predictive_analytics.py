import random
from datetime import datetime

def generate_health_score(job_history):
    return {
        "health_score": random.randint(40, 100),
        "risk_factors": random.sample([
            "High latency",
            "Frequent retries",
            "Credential expiration",
            "API rate limits"
        ], k=random.randint(0, 2)),
        "recommendations": random.sample([
            "Increase sync frequency",
            "Check database indexes",
            "Rotate API credentials",
            "Upgrade connection"
        ], k=random.randint(1, 3))
    }