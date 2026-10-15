"""
Docstring for task-manager.main
POC-01 : 
Title : Task Manager REST API
Problem Statement : Build a REST API to manage tasks (to-do items) for multiple projects.
Functional Requirements : 
• CRUD for Projects and Tasks (title, description, status, priority, due_date) Done
• Filter tasks by status/priority, sort by due date, pagination
• Pydantic request/response models with validation
• Routers split by resource; proper HTTP status codes
• In-memory or SQLite storage / or database

Tech Stack : Python, FastAPI, Pydantic v2, Uvicorn
Acceptance Criteria : All endpoints works and also from /docs.
Est. Effort : 2–3 days

"""

from models import Task, TaskUpdate, Project, ProjectUpdate
from fastapi import FastAPI, Depends
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()
database_models.Base.metadata.create_all(bind = engine)
#list of tasks in memory
tasks = [Task(id=1, title="Task 1", description="Complete Programming", status=False, priority=1, due_date="2024-06-30", project_id=1),
         Task(id=2, title="Task 2", description="Complete Testing", status=False, priority=2, due_date="2024-07-15", project_id=1),
         Task(id=3, title="Task 3", description="Complete Deployment", status=False, priority=3, due_date="2024-08-01", project_id=2)]

projects = [Project(id=1, title="Project 1", description="First Project"),
            Project(id=2, title="Project 2", description="Second Project")]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def db_init():
    db = session()
    count = db.query(database_models.Task).count
    if count == 0:
        for task in tasks:
            db.add(database_models.Task(**task.model_dump()))
        for project in projects:
            db.add(database_models.Project(**project.model_dump()))
        db.commit()
@app.get("/")
def greet():
    return {"message": "Welcome to the Task Manager API!"}

@app.get("/projects")
def get_all_projects(db: Session = Depends(get_db)):
    db_projects = db.query(database_models.Project).all()
    return db_projects

@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(database_models.Project).filter(database_models.Project.id == project_id).first()
    #project = next((p for p in projects if p.id == project_id), None)
    if not db_project:
        return {"error": "Project not found"}
    return {"Project": db_project}

@app.post("/project")
def create_project(project: Project, db: Session = Depends(get_db)):
    #Create a new project and add it to the list
    db_project = db.query(database_models.Project).filter(database_models.Project.id == project.id).first()
    db_project = database_models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    """ if any(p.id == project.id for p in projects):
        return {"error": "Project with this ID already exists"}
    projects.append(project) """
    return {"message": "Project created successfully", "project": project}

@app.put("/project/{project_id}")
def update_project(project_id: int, updated_project: ProjectUpdate, db: Session = Depends(get_db)):
    # Find the task with the given ID
    db_project = db.query(database_models.Project).filter(database_models.Project.id == project_id).first()
    #project = next((p for p in projects if p.id == project_id), None)
    if not db_project:
        return {"error": "Project not found"}
    if updated_project.title is not None:
        db_project.title = updated_project.title
    if updated_project.description is not None:
        db_project.description = updated_project.description
    db.commit()     
    return {"message": "project updated successfuly"}

@app.delete("/project/{project_id}")
def delete_product(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(database_models.Project).filter(database_models.Project.id == project_id).first()
    if not db_project:
        return {"error": "Project not found"}
    db.delete(db_project)
    db.commit()
    return {"message":"Project deleted successfuly"}
    """ for i in range(len(projects)):
        if project_id == projects[i].id:
            del project
            return {"message":"Project deleted successfuly"}
    return {"error": " Project not found"}"""

#Filter tasks by priority set
@app.get("/tasks/priority")
def get_tasks_by_priority(db: Session = Depends(get_db)):
    #Priority 1 highest after that 2 and then 3 but what if we added 4 or 5 then we need to sort by priority and return the tasks
    # Query MySQL and order by priority ascending (1, 2, 3, 4, 5...)
    db_tasks = db.query(database_models.Task).order_by(database_models.Task.priority.asc()).all()
    #sorted_tasks = sorted(tasks, key=lambda x: x.priority)
    return {"tasks_sorted_by_priority": db_tasks}

#Filter tasks by due date
@app.get("/tasks/due_date")
def get_tasks_by_due_date(db: Session = Depends(get_db)):
    # Query Mysql and order by due_date ascending (earliest first, None last)
    db_tasks = db.query(database_models.Task).order_by(database_models.Task.due_date.asc()).all()
    """def sort_key(task):
        return (task.due_date is None, task.due_date or "")

    sorted_tasks = sorted(tasks, key=sort_key)"""
    
    return {"tasks_sorted_by_due_date": db_tasks}

@app.get("/tasks")
def get_all_tasks(page:int = 1, limit:int =5, db: Session = Depends(get_db)):
    # All tasks are returned as a list of dictionaries
    #pagination logic
    db_tasks = db.query(database_models.Task).all()

    start = (page - 1)* limit
    end = start + limit
    return { "Page": page,
            "Limit": limit,
            "Total": len(db_tasks),
        "tasks": db_tasks[start: end]}

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    # Find the task with the given ID
    db_task = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
    #task = next((t for t in tasks if t.id == task_id), None)
    if not db_task:
        return {"error": "Task not found"}
    return {"task": db_task}

@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db)):
    # Check if the task with the same ID already exists
    db_task = db.query(database_models.Task).filter(database_models.Task.id == task.id).first()
    db_task = database_models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"message": "Task created successfuly", "task": db_task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db)):
    # Find the task with the given ID
    db_task = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
    #task = next((t for t in tasks if t.id == task_id), None)
    if not db_task:
        return {"error": "Task not found"}

    # Update only if a value was provided
    if updated_task.title is not None:
        db_task.title = updated_task.title
    if updated_task.description is not None:
        db_task.description = updated_task.description
    if updated_task.status is not None:
       db_task.status = updated_task.status
    if updated_task.priority is not None:
        db_task.priority = updated_task.priority
    if updated_task.due_date is not None:
        db_task.due_date = updated_task.due_date
    if updated_task.project_id is not None:
        db_task.project_id = updated_task.project_id
    db.commit()
    db.refresh(db_task)
    return {"message": "Task updated successfully", "task": db_task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
    if not db_task:
        return {"error": "Task not found"}
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
    """           del tasks[i]
            return {"message": "Task deleted successfully"}
    return {"message": "Task not deleted "}"""

#Fetch all tasks for a specific project
@app.get("/projects/{project_id}/tasks")
def get_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(database_models.Project).filter(database_models.Project.id == project_id).first()
    if not db_project:
        return {"error": "Project not found"}
    project_tasks = db.query(database_models.Task).filter(database_models.Task.project_id == project_id).all()
    if not project_tasks:
        return {"error": "No tasks found for this project"}
    return {"tasks": project_tasks}
