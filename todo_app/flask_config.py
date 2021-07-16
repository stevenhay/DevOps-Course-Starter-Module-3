import os

class Config:
    """Base configuration variables."""
    MONGO_URL = 'cluster0.brtrv.mongodb.net'
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_DATABASE = 'todoapp'
