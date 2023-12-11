from sqlalchemy import event
from sqlalchemy.engine import Engine
from db import SessionManager
from gui import reset_database, initialize_db, initialize_gui


# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


if __name__ == "__main__":
    sqlite_url = "sqlite:///university_evaluation.db"
    username = "cs5330"
    password = "cs5330"
    hostname = "localhost"
    db_name = "dbprog"
    port = 3306
    mysql_connection_string = (
        f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{db_name}"
    )
    db_manager = SessionManager(mysql_connection_string)
    reset_database(db_manager.engine)
    initialize_db(db_manager)
    initialize_gui()
