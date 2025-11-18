"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# SAT Prep app schemas

class Satclass(BaseModel):
    """
    SAT class/course details
    Collection name: "satclass"
    """
    title: str = Field(..., description="Course title")
    subtitle: Optional[str] = Field(None, description="Short tagline/subtitle")
    description: Optional[str] = Field(None, description="Overview description")
    highlights: List[str] = Field(default_factory=list, description="Key highlights")

class Plan(BaseModel):
    """
    Pricing plan for the SAT class
    Collection name: "plan"
    """
    name: str = Field(..., description="Plan name")
    price: float = Field(..., ge=0, description="Price in USD")
    frequency: str = Field(..., description="Billing frequency, e.g., per course, per month")
    features: List[str] = Field(default_factory=list, description="Included features")
    popular: bool = Field(False, description="Whether this is a popular plan")

class Review(BaseModel):
    """
    Reviews from students/parents
    Collection name: "review"
    """
    name: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    comment: str = Field(..., description="Review text")
    role: Optional[str] = Field(None, description="Student/Parent/Teacher")
