import os

from fastapi import FastAPI, HTTPException, Header, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import uvicorn

import var
import db
import model

app = FastAPI()

origins = [ "http://localhost:4200" ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"])

@app.get("/db/latest/database.db")
def get_database():
    print("return database to user")
    return False

@app.post("/api/set/device")
def set_device(payload:model.NewDevicePayload):
    success, reason = db.add_device(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/prefix")
def set_prefix(payload:model.NewItemPayload):
    print("set prefix")
    success, reason = db.add_prefix(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/model")
def set_model(payload:model.NewItemPayload):
    print("set model")
    success, reason = db.add_model(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/manufacturer")
def set_manufacturer(payload:model.NewItemPayload):
    print("set manufacturer")
    success, reason = db.add_manufacturer(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/control")
def set_control(payload:model.NewItemPayload):
    print("set control")
    success, reason = db.add_control(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/capability")
def set_control(payload:model.NewItemPayload):
    print("set capability")
    success, reason = db.add_capability(payload)
    return { "success":success, "reason":reason }

@app.post("/api/set/task")
def set_task(payload:model.NewItemPayload):
    print("set task")
    success, reason = db.add_task(payload)
    return { "success":success, "reason":reason }

@app.get("/api/get/prefixes")
def get_prefixes(prefix: str = None, manufacturer:str=None):
    payload = db.get_prefixes()
    return { "payload":payload, "type":"prefixes" }

@app.get("/api/get/manufacturers")
def get_manufacturers():
    payload = db.get_manufacturers()
    return { "payload":payload, "type":"manufacturers" }

@app.get("/api/get/models")
def get_models(model: str = None, manufacturer:str = None):
    payload = db.get_models(model, manufacturer)
    return { "payload":payload, "type":"models" }

@app.get("/api/get/capabilities")
def get_capabilities():
    payload = db.get_capabilities()
    return { "payload":payload, "type":"capabilities" }

@app.get("/api/get/controltypes")
def get_controltypes():
    payload = db.get_control_types()
    return { "payload":payload, "type":"controltypes" }

@app.get("/api/get/tasks")
def get_tasks():
    payload = db.get_tasks()
    return { "payload":payload, "type":"tasks" }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)