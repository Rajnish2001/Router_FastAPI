from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from blog.schemas import Blog,ShowBlog
from blog.database import SessionLocal,get_db
from blog import models


router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def blog(request:Blog,db:SessionLocal=Depends(get_db)):
    blog_data = models.Blog(title=request.title,blog=request.blog,creator_id=request.creator_id)
    db.add(blog_data)
    db.commit()
    db.refresh(blog_data)
    return blog_data


@router.get('/',response_model=List[ShowBlog],status_code=status.HTTP_200_OK)
def all_blog(db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@router.get('/{id}',response_model=ShowBlog,status_code=status.HTTP_200_OK)
def blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    db.delete(blog)
    db.commit()
    return 'Blog is deleted'