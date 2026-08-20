import json
import subprocess
import typer

# wrapper function so that command line option can be passed
def app():
       typer.run(main)

def pod_health(pod):
    if pod["status"]["phase"] != "Running":
        return False
    containers = pod["status"].get("containerStatuses", [])
    return all(c["ready"] for c in containers)

def pod_summary(pod):
    return {
        "name": pod["metadata"]["name"],
        "namespace": pod["metadata"]["namespace"],
        "phase": pod["status"]["phase"],
        "healthy": pod_health(pod),
    }

def main(only_failing: bool = False):    # <- the flag becomes a parameter
    result = subprocess.run(
        ["kubectl", "get", "pods", "-o", "json"],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)

    for pod in data["items"]:
        summary = pod_summary(pod)
        if only_failing and summary["healthy"]:
            continue
        print(summary)

if __name__ == "__main__":
    typer.run(main)
