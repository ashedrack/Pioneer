from sqlalchemy import Column, Integer, String
from app import db

class Resource(db.Model):
    id = Column(Integer, primary_key=True)
    resource_id = Column(String(50), unique=True)
    cpu_usage = Column(Integer)
    memory_usage = Column(Integer)
    disk_usage = Column(Integer)
    network_usage = Column(Integer)
