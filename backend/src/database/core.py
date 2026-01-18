import os
from typing import Annotated
from src.core.config import settings

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Create the engine using the DB URL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

# This is the configuration for each of the individual sessions made as each of those sessions will be a SessionLocal object so the class must be properly configured
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Now we make the declarative base which is essentially how SQLAlchemy knows that a given class is a database table or something because it will extend the Base
Base = declarative_base()

"""
Now this is the important part and why FastAPI is so good and it is the usage of generators. 
We essentially define objects like database connections that need to have their own sessions and need to be opened and closed
as generator functions. We then use fastapi and its dependency management systems (Depends) and Annotated to bind a generator function
to its target object so that whenever we instantiate that object, FastAPI automatically calls the generator and does next(gen) which runs
the generator until it encounters the yield object at which point execution is stopped, the object that is meant to be yielded is returned 
and until next is called again (handled automatically by FastAPI) execution will stay paused. When next is called for the second time, it will
execute the rest of the function which should ideally close the database in this case. We handle this with a try, finally block. 
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This is the type annotation we will use to start a DB session automatically; this is what we will import to other files from this file
DB_Session = Annotated[Session, Depends(get_db)]