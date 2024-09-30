from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from web import explorer, creature, user
import uvicorn

from typing import Generator

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


def get_file(path: str) -> Generator:
    with open(file=path, mode='rb') as file:
        yield file.read()


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
