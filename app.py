import os
import json
import uuid
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

# Import our custom modules
from logger import logger, perf_logger
from models import db, User, Task, init_db
import utils

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with our app
init_db(app)

# Request timing middleware
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    request_duration = time.time() - request.start_time
    request_id = str(uuid.uuid4())[:8]
    
    # Log request details
    log_data = {
        'request_id': request_id,
        'method': request.method,
        'path': request.path,
        'status': response.status_code,
        'duration': round(request_duration * 1000, 2),  # in ms
        'ip': request.remote_addr
    }
    
    # Log slow requests (>500ms) with higher severity
    if request_duration > 0.5:
        perf_logger.warning(f"SLOW REQUEST: {json.dumps(log_data)}")
    else:
        perf_logger.info(json.dumps(log_data))
    
    return response

# Routes
@app.route('/')
def home():
    logger.info("API root accessed")
    return jsonify({
        "message": "Task Manager API",
        "version": "1.0",
        "endpoints": [
            {"method": "GET", "path": "/api/users", "description": "Get all users"},
            {"method": "POST", "path": "/api/users", "description": "Create a new user"},
            {"method": "GET", "path": "/api/users/{username}/tasks", "description": "Get tasks for a specific user"},
            {"method": "POST", "path": "/api/users/{username}/tasks", "description": "Create a new task for a user"},
            {"method": "POST", "path": "/api/users/{username}/task/{task_id}/complete", "description": "Complete a task for user"}
        ]
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        return utils.get_users()
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to retrieve users"}), 500

@app.route('/api/users', methods=['POST'])
def create_user():    
    try:
        data = request.json
        if not data:
            logger.warning("Invalid request: No JSON data provided")
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get('username', None)
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        
        return jsonify(utils.add_user(name= username, email=email, phone_number=phone_number))
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to create user"}), 500

@app.route('/api/users/<username>/tasks', methods=['GET'])
def get_user_tasks(username):
    try:
        return jsonify(utils.get_user_tasks(username=username))
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {username}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to retrieve tasks"}), 500

@app.route('/api/users/<username>/tasks', methods=['POST'])
def create_task(username: str):
    try:
        # Check if user exists        
        data = request.json
        if not data:
            logger.warning("Invalid request: No JSON data provided")
            return jsonify({"error": "No data provided"}), 400
        
        title = data.get('title', None)
        description = data.get('description', None)
        completed = data.get('completed', None)
        priority = data.get('completed', None)
        
        return jsonify(utils.add_user_task(username, title, description, completed, priority))
    
    # except KeyError as e:
    #     db.session.rollback()
    #     logger.error(f"Missing required field: {str(e)}", exc_info=True)
    #     return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating task for user {username}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to create task"}), 500
    
@app.route('/api/users/<username>/task/<task_id>/complete', methods=['POST'])
def complete_task(username: str, task_id: int) :
    try :
        return jsonify(utils.complete_task(username, task_id))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing task for user {username}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to complete task"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path} not found")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    
    # Log unexpected errors
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    logger.info("Application starting")
    app.run(debug=True)