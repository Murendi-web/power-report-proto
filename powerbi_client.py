import json, os, datetime

class MockPowerBIClient:
    def push(self, rows):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"outputs/datasets/powerbi_push_{ts}.json"
        with open(path, "w") as f:
            json.dump(rows, f, indent=2)
        return path
