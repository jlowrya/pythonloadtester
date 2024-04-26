import time
import requests

class Response:
    def __init__(self, code, latency):
        self.code = code
        self.latency = latency


class LoadTest:
    def __init__(self, endpoint, duration):
        self.endpoint = endpoint
        self.duration = duration
        self.responses = []

    def test(self):
        print(f"Starting test of {self.endpoint} that will run for {self.duration} seconds...")
        start = time.time()

        while time.time() - start < self.duration:
            req_sent = time.time()
            resp = requests.get(self.endpoint)
            self.responses.append(Response(resp.status_code, (time.time()-req_sent)))

        print("Test complete")

tester = LoadTest("http://localhost:8080/test-api-main-endpoint", 30)
tester.test()
avg_latency = sum([resp.latency for resp in tester.responses])/len(tester.responses)

print(f"{len(tester.responses)} requests were sent in {tester.duration} seconds with an average latency of {round(avg_latency, 2)} s")

unique_resp_codes = set([resp.code for resp in tester.responses])
code_counts = {}
for code in unique_resp_codes:
    code_counts[code] = len([resp for resp in tester.responses if resp.code==code])
    print(f"{code_counts[code]} requests had a status code of {code}")

