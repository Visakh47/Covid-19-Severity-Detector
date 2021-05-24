import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer , Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Main code here

class UserAuth(Base):
    __tablename__ = "userauth"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

#SQLLite is serverless -> less space
if __name__ == '__main__':
    engine = create_engine('sqlite:///project_db.sqlite3')
    Base.metadata.create_all(engine)