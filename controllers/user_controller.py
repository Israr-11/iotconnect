from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session

from services.user_service import UserService
from config.database import get_db
from schemas.user_schema import UserCreate, UserUpdate, UserResponse

class UserController:
    def __init__(self):
        self.user_service = UserService()
    
    async def create_user(
        self, 
        user_data: UserCreate,
        db: Session
    ):
        """Create a new user"""
        user, error = self.user_service.create_user(db, user_data.dict())
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "User created successfully", "user": user.to_dict()}
    
    async def get_user(
        self, 
        user_id: int,
        db: Session
    ):
        """Get a user by ID"""
        user = self.user_service.get_user_by_id(db, user_id)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return {"user": user.to_dict()}
    
    async def get_all_users(
        self,
        db: Session
    ):
        """Get all users (admin function)"""
        users = self.user_service.get_all_users(db)
        return {"users": [user.to_dict() for user in users]}
    
    async def update_user(
        self, 
        user_id: int,
        user_data: UserUpdate,
        db: Session
    ):
        """Update a user"""
        user, error = self.user_service.update_user(db, user_id, user_data.dict(exclude_unset=True))
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "User updated successfully", "user": user.to_dict()}
    
    async def delete_user(
        self, 
        user_id: int,
        db: Session
    ):
        """Delete a user"""
        success, error = self.user_service.delete_user(db, user_id)
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        return {"message": "User deleted successfully"}