import os

from fastapi import FastAPI, HTTPException, Header, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import uvicorn

import var
import db

app = FastAPI()

origins = [ "http://localhost:4200" ]

app.add_middleware(CORSMiddleware, allow_origins=origins)

@app.get("/db/latest/database.db")
def get_database():
    print("return database to user")

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