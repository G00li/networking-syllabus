from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import json

class Task(BaseModel):
    id: int
    name: str
    description: str

def load_tasks():
    with open("tasks.json", "r") as file:
        return json.load(file)

tasks = load_tasks()

app = FastAPI()

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


@app.get("/")
def root():
    return {"Mensagem": "Bem vindo a API de tarefas!" }


@app.get("/tasks")
def getTasks():
    return tasks

@app.post("/tasks")
def createTask(task: Task):
    for existing_task in tasks:
        if existing_task["id"] == task.id:
            raise HTTPException(status_code=400, detail="Uma tarefa com esse ID já existe.")
    tasks.append(task.model_dump())
    save_tasks()
    return {"Mensagem": "Tarefa criada com sucesso", "Tarefa": task}

@app.put("/tasks/{taskId}")
def updateTask(taskId: int, updateTask: Task):
    if taskId != updateTask.id:
        raise HTTPException(status_code=400, detail="O ID na URL não corresponde ao ID da tarefa.")
    for i, task in enumerate(tasks):
        if task["id"] == taskId:
            tasks[i] = updateTask.model_dump()
            save_tasks()
            return {"Mensagem": "Tarefa atualizada com sucesso", "Tarefa": updateTask}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tasks/{taskId}")
def delete_product(taskId: int):
    for i, task in enumerate(tasks):
        if task["id"] == taskId:
            tasks.pop(i)
            save_tasks()
            return {"Mensagem": "Tarefa deletada"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")