from fastapi import FastAPI,Request,HTTPException,status,Depends
import socket
import redis
from models import Primary,Base
from database import engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import json

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

app=FastAPI()

db_dependency=Annotated[Session,Depends(get_db)]
cache_db = redis.Redis(host="redis", port=6379, db=0,decode_responses=True)

@app.middleware('http')
async def sample_middleware(request:Request,call_next):
    print("Before middleware")
    response=await call_next(request)
    print("after middle")
    return response

@app.get('/')
async def root():
    return {"message":"Home","id":socket.gethostname()}

@app.get('/set/{key}/{value}')
async def set_redis(key:str,value:str,db:db_dependency):
    if not key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Key is missing")
    new_data=Primary(
        token=key,
        file_path=value
        )
    db.add(new_data)
    db.commit()
    
@app.get('/get/{key}/')
async def get_redis(key:str,db:db_dependency):
    if not key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Key is missing")
    v = cache_db.get(key)
    if v:
        return cache_db.get(key)
    value=db.query(Primary).filter(Primary.token==key).first()
    if not value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"key {key} is not found")
    value_Dict={'id':value.id,'token':value.token,'file_path':value.file_path,"host-id":socket.gethostname()}
    cache_db.setex(f"{key}",300,json.dumps(value_Dict))
    return {f"{key}":value_Dict,"host-id":socket.gethostname()}