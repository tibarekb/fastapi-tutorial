from fastapi import FastAPI
# from .config import settings
from . import models
from .database import engine
from .routers import post, user, auth

#create a table using our model
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
    
'''   
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":
    "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p    
    
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return  i
''' 

'''
# Path Operation
@app.get("/") # this decorator makes this function a FastAPI
def root(): 
    return {"message": "Hello World"}
'''
    



