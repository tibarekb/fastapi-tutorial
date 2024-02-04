from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from .. import models
from .. import schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

#retrieve all the posts
# @router.get("/", response_model=List[schemas.PostOut]) # to retrieve data we use get method i.e HTTP METHOD
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results = db.query(models.Post, func.count(models.Vote.post_id)).join(models.Vote, models.Vote.post_id == models.Post.id, 
    #     isouter=True).group_by(models.Post.id).all()
    
    posts = posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


#create posts
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: str =  Depends(oauth2.get_current_user)): #Validate the entered data using the Model
    '''
    post_dict = post.dict()# print(post.dict()) #convert pydantic model to dictionary
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict) 
    # staging the changes
    
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() # to push the changes to postgresql
    '''
    # post.dict()
   
    new_post = models.Post(owner_id= current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve the commited data and store it on new_post again
    
    return new_post

#retrieve a data using id 
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    '''
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    '''
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).first()
    
    # post = find_post(id) #when a parameter is returned it is always a string.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    '''
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        '''
    # post = db.query(models.Post).first()
    return post

#delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the
    # index = find_index_post(id)
    '''
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    '''
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session = False)
    db.commit()
    
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update posts
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    ''' 
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published,str(id),))
    # index = find_index_post(id)
    updated_post = cursor.fetchone()
    conn.commit()
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()