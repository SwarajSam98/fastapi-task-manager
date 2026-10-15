from pydantic import BaseModel
from typing import Optional
# Main model (used for creating and returning tasks)
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False
    priority: int = 1
    due_date: str = None
    project_id: Optional[int] = None

# Update model (all fields optional, no 'id' needed)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None
    project_id: Optional[int] = None

# --- PROJECT MODELS ---

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    id: int
    title: str
    description: Optional[str] = None