from pydantic import BaseModel,model_validator,StrictBool

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
    title : str |None =None
    description : str |None=None
    completed : StrictBool |None=None
    
    @model_validator(mode="after")
    def reject_null_values(self):
        for field in self.model_fields_set:
            if getattr(self,field) is None:
                raise ValueError(f"{field} cannot be null")
        return self
    
    
