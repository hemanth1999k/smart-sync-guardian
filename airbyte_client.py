from dotenv import load_dotenv
import os
from mock_data import get_mock_jobs, get_mock_logs

load_dotenv()

class AirbyteClient:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        
    def get_active_syncs(self):
        return get_mock_jobs()
    
    def get_job_logs(self, job_id):
        return get_mock_logs(job_id)
    
    def trigger_resync(self, connection_id):
        return {"status": "success"}