from fastapi import APIRouter

rw_report = APIRouter()


@rw_report.get("/root")
async def root():
    return {"message": "Hello World"}


@rw_report.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
