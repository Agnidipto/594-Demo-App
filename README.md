# Demo Flask Application with Deliberate Bugs

This project is a demonstration REST API application with deliberately introduced bugs, errors, and inefficiencies to generate meaningful logs for testing RAG-based debugging systems.

## Project Overview

The application is a simple task management API that provides endpoints for:
- Managing users
- Creating and retrieving tasks
- Processing data
- Searching
- Debug endpoints that trigger specific errors

The application is designed to fail in various ways and generate rich, contextual logs that can be analyzed by an AI-powered debugging system.

## Project Structure

```
.
├── app.py              # Main application with API routes
├── models.py           # Database models and initialization
├── logger.py           # Logging configuration
├── requirements.txt    # Project dependencies
├── logs/               # Directory for log files
│   ├── app.log         # General application logs
│   ├── error.log       # Error-level logs
│   └── performance.log # Request timing and performance data
├── test_app.py         # Script to generate test traffic
├── log_reader.py       # Utility to read and analyze logs
└── log_monitor_rag.py  # Skeleton for RAG-based debugging system
```

## Deliberate Errors and Bugs

The application contains the following types of deliberate errors:

### Database and Connection Issues
- **Simulated timeouts** in `app.py` → `get_users()` function:
  ```python
  # Deliberate bug: occasional timeout simulation
  if random.random() < 0.1:  # 10% chance
      logger.warning("Simulating database timeout")
      time.sleep(3)
      # Sometimes succeed, sometimes fail
      if random.random() < 0.5:
          raise TimeoutError("Database connection timed out")
  ```

- **SQL injection vulnerability** in `app.py` → `create_user()` function:
  ```python
  # Check for existing user - deliberate bug in SQL query
  if random.random() < 0.15:  # 15% chance
      logger.debug("About to execute query with deliberate SQL error")
      existing_user = db.session.execute("SELECT * FROM user WHERE username = '" + data['username'] + "'").fetchone()
  ```

### Input Validation Issues
- **Missing validation** for required fields in `app.py` → `create_user()` function:
  ```python
  # Deliberate bug: missing required fields validation
  if 'username' not in data or 'email' not in data:
      # We won't handle this correctly, causing an error
      pass
  ```

- **Weak email validation** in `app.py` → `create_user()` function:
  ```python
  # Email validation - deliberate bug
  if not '@' in data.get('email', ''):
      logger.warning(f"Invalid email format: {data.get('email')}")
      return jsonify({"error": "Invalid email format"}), 400
  ```

### Performance Issues
- **Inefficient query** in `app.py` → `get_user_tasks()` function:
  ```python
  # Deliberate bug: inefficient query that might timeout
  if random.random() < 0.2:  # 20% chance
      logger.debug("Using inefficient query pattern")
      time.sleep(1)  # Simulate slow query
      
      # Memory inefficient approach
      all_tasks = Task.query.all()
      tasks = [task for task in all_tasks if task.user_id == user_id]
  ```

- **Slow search** in `app.py` → `search()` function:
  ```python
  # Deliberately inefficient search if query is too short
  if len(query) < 3:
      logger.warning(f"Short search query detected: '{query}'. This may cause performance issues.")
      
      # Simulate slow search for short queries
      time.sleep(1.5)
  ```

### Memory Issues
- **Memory leak simulation** in `app.py` → `process_data()` function:
  ```python
  # Simulated memory leak
  large_list = []
  for i in range(min(len(str(data)), 100000)):
      large_list.append(str(i) * 100)
  
  # Randomly fail for large operations
  if random.random() < 0.3:  # 30% chance
      logger.error("Memory error during processing large dataset")
      raise MemoryError("Insufficient memory for operation")
  ```

### Reference Errors
- **Non-existent field access** in `app.py` → `create_task()` function:
  ```python
  # Deliberate bug: sometimes we'll try to access a field that might not exist
  if random.random() < 0.15:  # 15% chance
      priority = data['priorityLevel']  # This key doesn't exist in client requests
      logger.debug(f"Attempting to access non-existent field: {priority}")
  ```

### Debug Endpoints
The application also provides endpoints that deliberately trigger various types of errors:

- `/api/debug?type=division`: Triggers a division by zero error
- `/api/debug?type=reference`: Triggers a reference error (undefined variable)
- `/api/debug?type=recursion`: Triggers a recursion depth error
- `/api/debug?type=memory`: Attempts to allocate a large amount of memory
- `/api/debug?type=generic`: Triggers a generic error

## Setting Up the Project

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

3. Generate test traffic:
   ```
   python test_app.py
   ```

4. View and analyze logs:
   ```
   python log_reader.py
   ```

5. Test the RAG-based debugging skeleton:
   ```
   python log_monitor_rag.py
   ```

## API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create a new user |
| GET | `/api/users/{user_id}/tasks` | Get tasks for a specific user |
| POST | `/api/users/{user_id}/tasks` | Create a new task for a user |
| POST | `/api/process` | Process data payload |
| GET | `/api/search?q={query}` | Search for users and tasks |
| GET | `/api/debug?type={error_type}` | Trigger deliberate errors for testing |

## Log Files

The application generates three types of log files:

- **app.log**: General application logs with all severity levels
- **error.log**: Error-level logs only
- **performance.log**: Request timing and performance data

These logs provide rich information about application state, errors, and performance issues that can be used to train and test RAG-based debugging systems.

## RAG-Based Debugging

The `log_monitor_rag.py` file provides a skeleton implementation for a RAG-based debugging system that:

1. Monitors log files for new error entries
2. Detects patterns of similar errors
3. Retrieves relevant code and past solutions via vector search (mocked)
4. Generates diagnostics and resolution steps (mocked)

You can extend this implementation with actual vector database connections, embedding generation, and language model integration to create a fully functional debugging system.