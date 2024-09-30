from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web import explorer, creature, user
from pathlib import Path
import uvicorn

from typing import Generator
from fake.creature import _creatures as fake_creatures
from fake.explorer import _explorers as fake_explorers

app = FastAPI()

top = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=f"{top}/template")

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


app.mount("/static", StaticFiles(directory=f"{top}/static", html=True), name="static")


def get_file(path: str) -> Generator:
    with open(file=path, mode='rb') as file:
        yield file.read()


@app.get("/list")
def explorer_list(request: Request):
    return template_obj.TemplateResponse("list.html",
                                         {
                                             "request": request,
                                             "explorers": fake_explorers,
                                             "creatures": fake_creatures
                                         })


@app.post("/who")
def greet(name: str = Form()):
    return f"Hello, {name}"


@app.post('/small')
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file_size: {len(small_file)}"


@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"file_size: {big_file.size}, name: {big_file.filename}"


@app.get("/small/{name}")
async def download_small_file(name):
    return FileResponse(name)


@app.get("/download_big/{name}")
async def download_big_file(name: str):
    gen_expr = get_file(path=name)
    response = StreamingResponse(content=gen_expr, status_code=200)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
