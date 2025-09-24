from sqlmodel import SQLModel, create_engine, Session

# Use SQLite for simplicity
DATABASE_URL = "sqlite:///./schemas.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Initialize the database and create tables."""
    from app.models import Application, Service, SchemaRecord
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a new database session."""
    return Session(engine)
