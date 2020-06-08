"""Starlette is a very fast python web framework, so in order to stress-test it effectively we have to use the locust distributed load testing framework ."""

from locust import HttpLocust, TaskSet, task, between


class StamperTaskSet(TaskSet):
    @task(6)
    def submit(self):
        with self.client.post(
            "/api/v1/submit",
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "submit",
                "params": {"checksum": "4eccf34608d31bac5c7becf6006df59005d828181056d092084e341e6bb005bd"},
            }, 
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("The stamp response was an eror")

    @task(5)
    def check_proof(self):
        with self.client.post(
            "/api/v1/proof",
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "proof",
                "params": {"checksum": "string"},
            }, 
                catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("The proof response was an eror")


class Stamper(HttpLocust):
    # host = 'http://localhost:5000'
    task_set = StamperTaskSet
    wait_time = between(0.1, 12)
