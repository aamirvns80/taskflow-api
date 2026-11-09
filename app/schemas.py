from pydantic import BaseModel

class TaskCreate(BaseModel):
    title:str
    description:str
    completed: bool = False
    
    
class TaskResponse(BaseModel):
    id : int
    title: str
    description: str
    completed: bool
    
class TaskUpdate(BaseModel):
    title:str
    description:str
    completed:bool
    
    
class TaskPatch(BaseModel):
    title : str | None =None
    description : str |None=None
    completed : bool |None=None
    
    
