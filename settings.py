import os

DATABASE_FILE_NAME = "db.sqlite"
DATABASE_PATH = f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/{DATABASE_FILE_NAME}"