from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Models
class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, db.CheckConstraint('priority >= 1 AND priority <= 5'), default=1)  # 1-5 scale
    
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'user_username': self.username,
            'completed': self.completed,
            'priority': self.priority
        }

def init_db(app):
    """Initialize the database, create tables and sample data"""
    from logger import logger
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Add some sample data if database is empty
        if User.query.count() == 0:
            logger.info("Initializing database with sample data")
            
            # Create sample users
            user1 = User(username="johndoe", email="john@example.com")
            user2 = User(username="janedoe", email="jane@example.com")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            
            # Create sample tasks
            task1 = Task(title="Complete project", description="Finish the Flask project", username="johndoe", priority=3)
            task2 = Task(title="Buy groceries", description="Milk, eggs, bread", username="johndoe", priority=2)
            task3 = Task(title="Learn Flask", description="Study Flask documentation", username="janedoe", priority=4)
            
            db.session.add_all([task1, task2, task3])
            db.session.commit()
            
            logger.info("Sample data created successfully")