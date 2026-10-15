from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:SwarajSam1998/@localhost:3306/task_db"
engine = create_engine(DATABASE_URL)
session = sessionmaker(autoflush= False, bind= engine)
