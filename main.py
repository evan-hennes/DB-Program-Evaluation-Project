from sqlalchemy import event
from sqlalchemy.engine import Engine
from db import SessionManager
from gui import reset_database, initialize_db, initialize_gui


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if __name__ == "__main__":
    db_manager = SessionManager("sqlite:///university_evaluation.db")
    reset_database()
    initialize_db(db_manager)
    initialize_gui()
