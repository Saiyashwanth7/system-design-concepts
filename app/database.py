from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLITE_URL='sqlite:///./db/primary.db'

engine= create_engine(SQLITE_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()
