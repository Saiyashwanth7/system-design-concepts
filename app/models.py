from database import Base
from sqlalchemy import String,Integer,Column

class Primary(Base):
    __tablename__='primary'
    id=Column(Integer,index=True,primary_key=True)
    token=Column(String)
    file_path=Column(String)