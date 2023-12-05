from sqlalchemy import event
from sqlalchemy.engine import Engine
from db import SessionManager
from gui import initialize_gui


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if __name__ == "__main__":
    db_manager = SessionManager
    initialize_gui(db_manager)
