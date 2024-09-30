import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
basic: HTTPBasicCredentials = HTTPBasic()


secret_user: str = "test_user"
secret_pass: str = "admin"


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_pass:
        return {"username": creds.username, "password": creds.password}
    else:
        raise HTTPException(status_code=401, detail="Not authorized")


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)