class Config:
    # Secret key protects user sessions and cookies
    SECRET_KEY = 'flask-secret-key-2024'

    # SQLite database file location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coursemanager.db'

    # Turn off modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug mode = shows errors clearly in browser
    DEBUG = True