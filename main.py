from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Witaj w świecie RESTP API"}

@app.get("/hello/{name}")
def say_hello(name: str, age: int = 18):
    return{
        "message": f"Witaj {name}",
        "info": f"Masz {age} lat"
    }