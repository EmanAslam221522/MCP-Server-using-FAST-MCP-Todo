#!/usr/bin/env python3
"""
FastAPI Todo Application with SQLite Database
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db, Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="A simple Todo API with SQLite database",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Todo API",
        "endpoints": {
            "docs": "/docs",
            "todos": "/todos",
            "health": "/health"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Create a new todo
@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item"""
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all todos with optional filters
@app.get("/todos", response_model=List[TodoResponse])
def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all todos with optional filtering"""
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if priority:
        query = query.filter(Todo.priority == priority)

    todos = query.offset(skip).limit(limit).all()
    return todos

# Get a specific todo by ID
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update a todo
@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo item"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

# Delete a todo
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return None

# Mark todo as complete
@app.post("/todos/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Mark a todo as completed"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = True
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

# Get statistics
@app.get("/todos/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    """Get todo statistics"""
    total = db.query(Todo).count()
    completed = db.query(Todo).filter(Todo.completed == True).count()
    pending = total - completed

    high_priority = db.query(Todo).filter(Todo.priority == "high", Todo.completed == False).count()
    medium_priority = db.query(Todo).filter(Todo.priority == "medium", Todo.completed == False).count()
    low_priority = db.query(Todo).filter(Todo.priority == "low", Todo.completed == False).count()

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "pending_by_priority": {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)