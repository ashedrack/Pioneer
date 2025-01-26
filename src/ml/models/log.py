from sqlalchemy import Column, Integer, String, DateTime
from app import db

class Log(db.Model):
    id = Column(Integer, primary_key=True)
    log_message = Column(String(255))
    timestamp = Column(DateTime)
