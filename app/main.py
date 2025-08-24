from fastapi import FastAPI
import socket
app=FastAPI()

@app.get('/')
async def root():
    return {"message":"Home","id":socket.gethostname()}