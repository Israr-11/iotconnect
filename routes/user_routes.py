from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from controllers.user_controller import UserController
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from config.database import get_db 


router = APIRouter()
user_controller = UserController()

@router.post("/", response_model=dict)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return await user_controller.create_user(user_data, db)

@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    return await user_controller.get_user(user_id, db)

@router.get("/", response_model=dict)
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users (admin function)"""
    return await user_controller.get_all_users(db)

@router.patch("/{user_id}", response_model=dict)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update a user"""
    return await user_controller.update_user(user_id, user_data, db)

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    return await user_controller.delete_user(user_id, db)