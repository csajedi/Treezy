"""Starlette is a very fast python web framework, so in order to stress-test it effectively we have to use the locust distributed load testing framework ."""

from locust import HttpLocust, TaskSet, SequentialTaskSet, task, between
import hashlib
import math


class StamperTaskSet(SequentialTaskSet):
    @task
    def submit(self):
        m = hashlib.sha256()
        m.update(math.random(10000))
        self.digest = self.hash.hexdigest()
        with self.client.post(
            "/api/v1/submit",
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "submit",
                "params": {"checksum": self.digest},
            }, 
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("The stamp response was an eror")

    @task
    def check_proof(self):
        with self.client.post(
            "/api/v1/proof",
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "proof",
                "params": {"checksum": self.digest},
            }, 
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("The proof response was an eror")


class Stamper(HttpLocust):
    # host = 'http://localhost:5000'
    task_set = StamperTaskSet
    wait_time = between(0.1, 12)
