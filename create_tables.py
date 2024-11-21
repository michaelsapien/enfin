from database import engine
import models

# Create tables in the database
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
