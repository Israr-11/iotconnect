from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Tuple, Any
from models.user import User

class UserService:
    def create_user(self, db: Session, user_data: Dict[str, Any]) -> Tuple[Optional[User], Optional[str]]:
        """Create a new user"""
        existing_user = db.query(User).filter(User.email == user_data['email']).first()
        if existing_user:
            return None, "Email already registered"
            
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            role=user_data.get('role', 'user')
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user, None
        
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
        
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
        
    def get_all_users(self, db: Session) -> List[User]:
        """Get all users"""
        return db.query(User).all()
        
    def update_user(self, db: Session, user_id: int, update_data: Dict[str, Any]) -> Tuple[Optional[User], Optional[str]]:
        """Update user information"""
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None, "User not found"
            
        # UPDATING ALLOWED FIELDS
        if 'name' in update_data:
            user.name = update_data['name']
        if 'role' in update_data:
            user.role = update_data['role']
            
        db.commit()
        db.refresh(user)
        
        return user, None
        
    def delete_user(self, db: Session, user_id: int) -> Tuple[bool, Optional[str]]:
        """Delete a user"""
        print(f"Attempting to delete user with ID: {user_id}")
        user = self.get_user_by_id(db, user_id)
        print(f"User found: {user}")
        if not user:
            return False, "User not found"
            
        db.delete(user)
        db.commit()
        
        return True, None