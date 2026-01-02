from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status


app = FastAPI()

class User(BaseModel):
    id : int
    username: str = Field(...,min_length=3)
    email: str
    is_active: bool = True
    bio: Optional[str] = None

items: List[User] = []
    
@app.get("/items", response_model=List[User])
def get_items():
    return items

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: User):
    for u in items:
        if u.id == item.id:
            raise HTTPException(status_code=400, detail="Osoba o takim ID juz istnieje")
    items.append(item)
    return item

@app.get("/items/count")
def count_activeitems(active: bool = True):
    count = 0
    for u in items:
        if u.is_active == active:
            count += 1
            
    return {"warunek": active, "count": count}

@app.get("/items/{user_id}", response_model=User)
def get_item(user_id: int):
    for u in items:
        if u.id == user_id:
            return u
    
    raise HTTPException(status_code=404, detail="Not Found")

@app.delete("/items/{user_id}")
def delete_item(user_id: int):
    global items
    
    initial_len = len(items)
    
    items = [u for u in items if u.id != user_id]
    
    if len(items) == initial_len:
        raise HTTPException(status_code=404,detail="Osoba nie znaleziona")
    
    return
    