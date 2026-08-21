from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()          # application object — endpoints attach to it

@app.get("/")            # when someone GETs the / path, run the function below
def root():
    return {"status": "ok"}      # return a dict — FastAPI turns it into JSON for you

@app.get("/health")
def health():
    return {"healthy": True}

@app.get("/version")
def health():
    return {"version": "0.1.0"}

class PodCheck(BaseModel):          # a model = the shape of expected data
    name: str                       # required, must be a string
    namespace: str = "default"      # optional, defaults to "default" if omitted
    replicas: int                   # required, must be an integer

@app.post("/check")                 # note: POST, not GET — we're receiving data
def check(pod: PodCheck):           # FastAPI sees the type and validates for you
    return {
        "received": pod.name,
        "namespace": pod.namespace,
        "replicas_doubled": pod.replicas * 2,   # proof it's a real int, not a string
    }