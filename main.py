from sqlalchemy import create_engine
from db import Base
from gui import initialize_gui

engine = create_engine("sqlite:///university_evaluation.db")

Base.metadata.create_all(engine)

if __name__ == "__main__":
    initialize_gui()
