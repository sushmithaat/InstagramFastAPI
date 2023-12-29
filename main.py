import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import auth.authentication
from db import models
from db.database import engine
from routers import user, post, comment

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(auth.authentication.router)


@app.get("/hello")
def get_hello():
    return {"message": "Hello World"}


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)
app.mount("/images", StaticFiles(directory="images"), name="images")
if __name__ == "__main__":
    uvicorn.run(app)
