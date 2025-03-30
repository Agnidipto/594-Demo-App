from models import db, User, Task, init_db
from logger import logger

def get_users() -> list[dict]:
  logger.info('Retrieving list of users')
  users_list: list[User] = db.session.query(User).all()
  users = [user.to_dict() for user in users_list]
  return users

def add_user(name: str, email: str, phone_number: str) -> dict:
  user = User(username=name, email=email, phone_number=phone_number)
  logger.info('Received user: ', user.to_dict())
  db.session.add(user)
  db.session.commit()
  logger.info('User Added: ', user.username)
  return {"success": True, "data": user.to_dict()}

def get_user_tasks(username: str) -> list[dict] :
  logger.info(f'Received username: {username}')
  logger.info(f'Retrieving user: {username}')
  user: User | None = db.session.query(User).filter(User.username == username).first()
  if user:
    logger.info('Found User')
  else :
    logger.error(f'No user found with username {username}')
    
  tasks_list: list[Task] = db.session.query(Task).filter(Task.username == user.username).all()
  tasks: list[dict] = [task.to_dict() for task in tasks_list]
  return tasks

def add_user_task(username: str, title: str, description: str, completed: bool= False, priority: int= 1) -> dict:
  logger.info('Attempting to add tasks to user')
  logger.info(f'Received username: {username}')
  logger.info(f'Retrieving user: {username}')
  user: User | None = db.session.query(User).filter(User.username == username).first()
  if not user:
    logger.error(f'No user found with username {username}')
    
  task = Task(title=title, description=description, username=user.username, completed=completed, priority=priority)
  logger.info(f'Received Task {task.to_dict()}')
  db.session.add(task)
  db.session.commit()
  return {'success': True, 'data': task.to_dict()}

def complete_task(username: str, task_id: int) :
  logger.info('Attempting to mark task as completed')
  logger.info(f'Received username: {username}')
  logger.info(f'Retrieving user: {username}')
  user: User | None = db.session.query(User).filter(User.username == username).first()
  if not user:
    logger.error(f'No user found with username {username}')
    
  logger.info(f'Received task_id: {task_id}')
  logger.info(f'Retrieving task_id: {task_id}')
  task: Task | None = db.session.query(Task).filter(Task.username == username, Task.task_id == task_id).first()
  if not task:
    logger.error(f'No task found with the task id {task_id} for user with username {username}')
  
  task.completed = True
  db.session.commit()
  return {'success': True, 'data': task.to_dict()}
  


  