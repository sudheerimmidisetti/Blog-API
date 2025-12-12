# crud.py
from sqlalchemy.orm import Session, joinedload
import models, schemas

# --- Author Logic ---

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_author_by_email(db: Session, email: str):
    return db.query(models.Author).filter(models.Author.email == email).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, email=author.email)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
        return True
    return False

def update_author(db: Session, author_id: int, author_data: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if db_author:
        db_author.name = author_data.name
        db_author.email = author_data.email
        db.commit()
        db.refresh(db_author)
    return db_author

# --- Post Logic ---

def create_post(db: Session, post: schemas.PostCreate):
    # Note: Validation for existing author happens in main.py
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Eager load the author relationship immediately for the response
    # This ensures the response schema can populate the nested 'author' field
    db.refresh(db_post) 
    return db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == db_post.id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100, author_id: int = None):
    query = db.query(models.Post)
    
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    # OPTIMIZATION: joinedload(models.Post.author)
    # This creates a single SQL JOIN query.
    # Without this, iterating over posts would trigger a new SQL query 
    # for every single post to fetch the author (N+1 problem).
    return query.options(joinedload(models.Post.author)).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    # Also using joinedload here for efficiency
    return db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == post_id).first()

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False

def update_post(db: Session, post_id: int, post_data: schemas.PostBase):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db_post.title = post_data.title
        db_post.content = post_data.content
        db.commit()
        db.refresh(db_post)
        # Refresh with relationship for correct response
        return db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == post_id).first()
    return None