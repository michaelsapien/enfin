from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from datetime import time

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Open a session
db = SessionLocal()

# Insert dummy users
user1 = models.User(name="User 1", timezone="UTC")
user2 = models.User(name="User 2", timezone="UTC")
db.add(user1)
db.add(user2)

# Insert weekly availability
weekly_availabilities = [
    models.WeeklyAvailability(user_id=1, day_of_week=0, start_time=time(9, 0), end_time=time(17, 0)),
    models.WeeklyAvailability(user_id=1, day_of_week=1, start_time=time(8, 0), end_time=time(12, 0)),
    models.WeeklyAvailability(user_id=2, day_of_week=0, start_time=time(10, 0), end_time=time(15, 0)),
    models.WeeklyAvailability(user_id=2, day_of_week=1, start_time=time(13, 0), end_time=time(17, 0))
]
db.add_all(weekly_availabilities)

# Commit the changes
db.commit()
db.close()

print("Dummy data inserted successfully!")
