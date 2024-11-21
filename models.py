
from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    timezone = Column(String)

class WeeklyAvailability(Base):
    __tablename__ = "weekly_availability"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_of_week = Column(Integer)  # 0=Monday, ..., 6=Sunday
    start_time = Column(Time)
    end_time = Column(Time)



class SpecificAvailability(Base):
    __tablename__ = "specific_availability"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

class ScheduledEvent(Base):
    __tablename__ = "scheduled_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
