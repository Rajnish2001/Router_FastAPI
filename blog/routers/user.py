from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from blog.schemas import User,ShowUser
from blog.database import SessionLocal,get_db
from blog import models
from blog.hashing import Hash

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post('/',response_model=ShowUser,status_code=status.HTTP_200_OK)
def user(request:User,db:SessionLocal=Depends(get_db)):
    # hash_password = pwd_context.hash(request.password)
    user = models.User(name=request.name,email=request.email,password=Hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/',response_model=List[ShowUser],status_code=status.HTTP_200_OK)
def all_user(db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.get('/{id}',response_model=ShowUser,status_code=status.HTTP_200_OK)
def user(id,db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'User id {id} is Not Found!')
    return user

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id,db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'User id {id} is Not Found!')
    db.delete(user)
    db.commit()
    return 'User is deleted'