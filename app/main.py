from fastapi import FastAPI,Request
import socket
import redis

app=FastAPI()

r = redis.Redis(host="redis", port=6379, db=0)

@app.get("/set/{key}/{value}")
def set_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Key '{key}' set to '{value}'"}

@app.get("/get/{key}")
def get_value(key: str):
    value = r.get(key)
    return {"key": key, "value": value.decode() if value else None}

@app.middleware('http')
async def sample_middleware(request:Request,call_next):
    print("Before middleware")
    response=await call_next(request)
    print("after middle")
    return response

@app.get('/')
async def root():
    return {"message":"Home","id":socket.gethostname()}