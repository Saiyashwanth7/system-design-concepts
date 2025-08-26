from fastapi import FastAPI,Request
import socket

app=FastAPI()

@app.middleware('http')
async def sample_middleware(request:Request,call_next):
    print("Before middleware")
    response=await call_next(request)
    print("after middle")
    return response

@app.get('/')
async def root():
    return {"message":"Home","id":socket.gethostname()}