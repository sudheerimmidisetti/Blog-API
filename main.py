# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

# Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", description="A RESTful API for managing authors and posts.")

# --- AUTHOR ENDPOINTS ---

@app.post("/authors", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_author(db=db, author=author)

@app.get("/authors", response_model=List[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.put("/authors/{author_id}", response_model=schemas.AuthorResponse)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    updated_author = crud.update_author(db, author_id, author)
    if updated_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author

@app.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    success = crud.delete_author(db, author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return None

# --- POST ENDPOINTS ---

@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Validate Author Existence
    author = crud.get_author(db, author_id=post.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author ID does not exist")
    return crud.create_post(db=db, post=post)

@app.get("/posts", response_model=List[schemas.PostResponse])
def read_posts(
    skip: int = 0, 
    limit: int = 100, 
    author_id: int = Query(None, description="Filter by Author ID"), 
    db: Session = Depends(get_db)
):
    # This endpoint handles the N+1 problem via logic in crud.py
    return crud.get_posts(db, skip=skip, limit=limit, author_id=author_id)

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    success = crud.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return None

# --- NESTED RESOURCE ENDPOINT ---

@app.get("/authors/{author_id}/posts", response_model=List[schemas.PostResponse])
def read_author_posts(author_id: int, db: Session = Depends(get_db)):
    # Validate author exists first
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Reuse get_posts logic which already includes optimized loading
    return crud.get_posts(db, author_id=author_id)