from fastapi import FastAPI
from app.core.service import Service

app = FastAPI()
svc = Service()

@app.post("/create-file")
def create_file(path: str, content: str):
    return svc.create_text_file(path, content)

@app.post("/update-file")
def update_file(path: str, content: str):
    return svc.update_text_file(path, content)

@app.post("/create-folder")
def create_folder(path: str):
    return svc.create_folder(path)

@app.post("/move")
def move(source: str, destination: str):
    return svc.move_or_rename_item(source, destination)

@app.post("/delete")
def delete(path: str):
    return svc.delete_item(path)

@app.get("/meta")
def meta(path: str):
    return svc.graph.resolve_by_path(path)
