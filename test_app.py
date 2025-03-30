import requests
import random
import json

BASE_URL = "http://localhost:5000"

# List of valid and invalid usernames for testing
valid_users = ["johndoe", "janedoe"]
invalid_users = ["nonexistent", "fakeuser", "testuser123"]

# Function to make API calls
def make_api_call(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
        
        print(f"{method} {url} - Status: {response.status_code}")
        return response
    except Exception as e:
        print(f"Error making {method} request to {url}: {str(e)}")
        return None

# Define various API calls - both valid and invalid
api_calls = [
    # Successful calls
    lambda: make_api_call("/api/users", "GET"),  # Get all users
    lambda: make_api_call("/api/users", "POST", {"username": f"user_{random.randint(1000, 9999)}", "email": f"user{random.randint(1000, 9999)}@example.com", "phone_number": f"+1{random.randint(1000000000, 9999999999)}"}),  # Create valid user
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "GET"),  # Get tasks for valid user
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": f"Task {random.randint(1, 100)}", "description": "This is a test task", "completed": False, "priority": random.randint(1, 5)}),  # Create valid task
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/task/1/complete", "POST"),  # Complete task 1 for valid user
    
    # Error-generating calls
    lambda: make_api_call("/api/nonexistent", "GET"),  # 404 error - endpoint doesn't exist
    lambda: make_api_call("/api/users", "POST", {}),  # Missing required fields
    lambda: make_api_call("/api/users", "POST", {"username": None, "email": "invalid"}),  # Invalid email format
    lambda: make_api_call(f"/api/users/{random.choice(invalid_users)}/tasks", "GET"),  # User doesn't exist
    lambda: make_api_call(f"/api/users/{random.choice(invalid_users)}/tasks", "POST", {"title": "Task", "description": "Test"}),  # Creating task for non-existent user
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/task/999/complete", "POST"),  # Task ID doesn't exist
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": None}),  # Missing required task field
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"priority": 10}),  # Invalid priority value
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/task/abc/complete", "POST"),  # Invalid task ID format
]

# Add some more random API call variations to reach 30 total calls
additional_calls = [
    # More successful calls
    lambda: make_api_call("/", "GET"),  # Access API root
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": "Priority Task", "description": "High priority task", "priority": 5}),
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": "Completed Task", "description": "Already done", "completed": True}),
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/task/2/complete", "POST"),
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/task/3/complete", "POST"),
    
    # More error-generating calls
    lambda: make_api_call("/api/users/1", "GET"),  # Using ID instead of username
    lambda: make_api_call("/api/users", "POST", {"username": random.choice(valid_users), "email": "duplicate@example.com"}),  # Duplicate username
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}", "DELETE"),  # Method not allowed
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"description": "Missing title field"}),
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": "Task with extremely long description" * 1000}),  # Extremely long description
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", {"title": "", "description": ""}),  # Empty values
    lambda: make_api_call(f"/api/users/{random.choice(valid_users)}/tasks", "POST", None),  # No JSON data
]

# Combine all calls
all_calls = api_calls + additional_calls

# Randomly shuffle and select 30 calls (15 successful, 15 error-generating)
random.shuffle(all_calls)
selected_calls = all_calls[:30]

# Execute the selected API calls
print("Making 30 API calls (15 successful, 15 error-generating)...\n")
for i, call in enumerate(selected_calls, 1):
    print(f"Call {i}:")
    call()
    print()

print("API testing completed.")