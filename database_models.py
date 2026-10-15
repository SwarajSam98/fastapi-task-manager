from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
Base = declarative_base()
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title= Column(String(255))
    description = Column(String(255))
    status = Column(Boolean, default=False)
    priority = Column(Integer, default=1)
    due_date = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255), nullable=True)