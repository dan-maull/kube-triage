from kube_triage.main import pod_health

def test_healthy_pod():
    pod = {
        "status": {
            "phase": "Running",
            "containerStatuses": [
                {"ready": True},
            ],
        }
    }
    assert pod_health(pod) == True

def test_broken_pod():
    pod = {
        "status": {
            "phase": "Running",
            "containerStatuses": [
                {"ready": False},
            ],
        }
    }
    assert pod_health(pod) == False

def test_pending_pod_no_container_statuses():
    pod = {
        "status": {
            "phase": "Pending",
            # note: NO containerStatuses key at all — like your day-one nginx
        }
    }
    assert pod_health(pod) == False