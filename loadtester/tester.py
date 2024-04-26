import time
import requests
from threading import current_thread, local
import concurrent.futures
from statistics import quantiles
from typing import NamedTuple

Response = NamedTuple("Response", [("code", int), ("latency", float)])

thread_local = local()

class LoadTest:
    def __init__(self, endpoint, duration):
        self.endpoint = endpoint
        self.duration = duration
        self.responses = []

    def test(self, session):
        thread = current_thread()
        print(f"{thread.name} : Starting test of {self.endpoint} that will run for {self.duration} seconds...")
        start = time.time()

        while time.time() - start < self.duration:
            req_sent = time.time()
            resp = session.get(self.endpoint)
            self.responses.append(Response(resp.status_code, (time.time()-req_sent)))

        print(f"{thread.name} : Test complete")

    @property
    def response_code_counts(self):
        by_code = {}
        unique_codes = set([resp.code for resp in self.responses])
        for code in unique_codes:
            by_code[code] = len([resp.code for resp in self.responses if resp.code==code])
        return by_code
    
    @property
    def latencies(self):
        return [resp.latency for resp in self.responses]
    
    @property
    def num_successful(self):
        return len([resp.code for resp in self.responses if resp.code==200])
    
    @property
    def num_failed(self):
        return len([resp.code for resp in self.responses if resp.code!=200])
    

class TestCoordinator:
    def __init__(self, concurrent_requests, duration):
        self.concurrent_requests = concurrent_requests
        self.duration = duration
        self.tests = []

    def run_tests(self, endpoint):
        self.tests = [LoadTest(endpoint,self.duration) for i in range(self.concurrent_requests)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
            executor.map(self.__run_individual_test, self.tests)
        print("All tests have completed.")

    def __get_session(self):
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session
 
    def __run_individual_test(self, load_test):
        session = self.__get_session()
        load_test.test(session)

    @property
    def total_requests(self):
        return sum([len(test.responses) for test in self.tests])
    
    @property
    def status_counts(self):
        counts = {}
        for test in self.tests:
            for key, value in test.response_code_counts.items():
                counts.setdefault(key, 0)
                counts[key] += value
        return counts

    @property
    def latencies(self):
        latencies = []
        for test in self.tests:
            latencies.extend(test.latencies)
        return latencies
    
    @property
    def throughput(self):
        return round(sum([test.num_successful for test in self.tests])/self.duration, 2)
    
    @property
    def num_successful(self):
        return sum([test.num_successful for test in self.tests])
    
    @property
    def num_failed(self):
        return sum([test.num_failed for test in self.tests])
    
    @property
    def latency_median(self):
        return quantiles(self.latencies, n=100)[49]
    
    @property
    def latency_95(self):
        return quantiles(self.latencies, n=100)[94]

    @property
    def latency_99(self):
        return quantiles(self.latencies, n=100)[98]

run = True

while run:
    threads = int(input("How many threads would you like to use?"))
    seconds = int(input("How many seconds would you like to run the test for?"))
    coordinator = TestCoordinator(threads, seconds)
    start = time.time()
    coordinator.run_tests("http://localhost:8080/test-api-main-endpoint")
    print(f"Finished processing {coordinator.total_requests} requests in {time.time()-start} seconds")
    print(f"Status code counts: {coordinator.status_counts}")
    print(f"Median latency: {coordinator.latency_median} seconds")
    print(f"95 latency: {coordinator.latency_95} seconds")
    print(f"99 latency: {coordinator.latency_99} seconds")
    print(f"Throughput is {coordinator.throughput} QPS and a success rate of {round(coordinator.num_successful/coordinator.total_requests*100)} %")
    resp = input("Would you like to run another test (y/n)?").lower()
    run = resp=="y"

