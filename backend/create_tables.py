from database import engine, Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)
print("✅ Tables Created Successfully!")
