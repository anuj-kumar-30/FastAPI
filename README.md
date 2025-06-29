# FastAPI Study Notes
Learning FastAPI from basic, with CampusX YouTube channel

## Table of Contents
1. [Introduction to FastAPI](#introduction-to-fastapi)
2. [FastAPI Philosophy](#fastapi-philosophy)
3. [Basic Setup and Installation](#basic-setup-and-installation)
4. [Core Concepts](#core-concepts)
5. [Code Analysis](#code-analysis)
6. [API Endpoints](#api-endpoints)
7. [Best Practices](#best-practices)
8. [Running the Application](#running-the-application)

## Introduction to FastAPI

It is a modern, high-performance web framework for building APIs with python.<br>
FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers:
- **High Performance**: Comparable to NodeJS and Go
- **Fast to Code**: Increase development speed by 200-300%
- **Fewer Bugs**: Reduce human-induced errors by ~40%
- **Intuitive**: Great editor support with autocompletion
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Production-ready code with automatic interactive documentation

## FastAPI Philosophy

FastAPI is built around two core principles that make it exceptional:

### 1. FastAPI is Fast to Code

**Why FastAPI accelerates development speed by 200-300%:**

#### **A. Minimal Boilerplate Code**
```python
# Traditional Flask approach (more verbose)
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Manual validation
    if not isinstance(user_id, int):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    # Manual serialization
    user = {'id': user_id, 'name': 'John Doe'}
    return jsonify(user)

# FastAPI approach (concise and automatic)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

@app.get('/users/{user_id}')
def get_user(user_id: int) -> User:
    return User(id=user_id, name='John Doe')
```

#### **B. Automatic Data Validation**
- **Type Hints Integration**: Python type hints are used for automatic validation
- **Pydantic Models**: Automatic JSON serialization/deserialization
- **Built-in Error Handling**: Automatic 422 validation errors with detailed messages
- **No Manual Validation**: Eliminates repetitive validation code

#### **C. Automatic Documentation Generation**
- **OpenAPI/Swagger**: Automatic API documentation at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **Interactive Testing**: Test endpoints directly from documentation
- **Schema Generation**: Automatic request/response schema generation

#### **D. IDE Support and Autocompletion**
- **Type Safety**: Full IDE autocompletion and type checking
- **IntelliSense**: Real-time code suggestions and error detection
- **Refactoring Support**: Safe code refactoring with type checking
- **Debugging**: Better debugging experience with type information

#### **E. Declarative Syntax**
```python
# FastAPI's declarative approach
@app.get('/items/{item_id}', response_model=Item, status_code=200)
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 2. FastAPI is Fast to Run

**Why FastAPI achieves high performance comparable to NodeJS and Go:**

#### **A. Starlette Foundation**
- **ASGI Framework**: Built on Starlette, a lightweight ASGI framework
- **Async/Await Support**: Native async/await for non-blocking I/O
- **High Concurrency**: Handles thousands of concurrent connections
- **Event Loop Optimization**: Efficient event loop management

#### **B. Pydantic Performance**
- **Rust-based Validation**: Core validation written in Rust for speed
- **Compiled Validation**: Validation rules are compiled for faster execution
- **Memory Efficient**: Optimized memory usage for large datasets
- **Lazy Evaluation**: Validation only when needed

#### **C. Uvicorn ASGI Server**
```python
# High-performance ASGI server
uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
```
- **Multiple Workers**: Process-based concurrency
- **HTTP/2 Support**: Modern HTTP protocol support
- **WebSocket Support**: Real-time communication capabilities
- **Optimized for Python**: Specifically tuned for Python performance

#### **D. Performance Benchmarks**
| Framework | Requests/sec | Latency (ms) |
|-----------|-------------|--------------|
| FastAPI   | ~50,000     | ~2.5         |
| Flask     | ~15,000     | ~8.0         |
| Django    | ~12,000     | ~10.0        |
| Express   | ~45,000     | ~3.0         |

#### **E. Technical Performance Features**

**1. Dependency Injection System**
```python
# Fast dependency resolution
def get_db():
    return Database()

@app.get('/users/')
def read_users(db: Database = Depends(get_db)):
    return db.get_users()
```

**2. Background Tasks**
```python
# Non-blocking background operations
@app.post('/send-notification/')
async def send_notification(
    background_tasks: BackgroundTasks,
    email: str
):
    background_tasks.add_task(send_email, email)
    return {"message": "Notification sent"}
```

**3. Response Streaming**
```python
# Efficient streaming responses
@app.get('/stream/')
async def stream_response():
    async def generate():
        for i in range(1000):
            yield f"data: {i}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")
```

#### **F. Memory and CPU Optimization**
- **Lazy Loading**: Components loaded only when needed
- **Connection Pooling**: Efficient database connection management
- **Caching Support**: Built-in caching mechanisms
- **Garbage Collection**: Optimized memory management

### **Why These Philosophies Matter**

#### **For Development Teams:**
- **Reduced Time-to-Market**: Faster development cycles
- **Lower Maintenance**: Less code to maintain and debug
- **Better Documentation**: Automatic, always-updated docs
- **Team Productivity**: Consistent patterns and tooling

#### **For Production Systems:**
- **Scalability**: Handle high traffic with minimal resources
- **Reliability**: Fewer bugs and better error handling
- **Monitoring**: Built-in metrics and observability
- **Cost Efficiency**: Lower server costs due to performance

#### **For API Consumers:**
- **Better Developer Experience**: Clear documentation and examples
- **Faster Response Times**: Optimized performance
- **Consistent Error Handling**: Standardized error responses
- **Interactive Testing**: Try APIs directly from documentation

This dual philosophy of "fast to code" and "fast to run" makes FastAPI uniquely positioned for modern API development, combining developer productivity with production performance.

## Basic Setup and Installation

### Prerequisites
- Python 3.7+
- Package manager (pip or uv)

### Installation
```bash
# Using pip
pip install fastapi uvicorn[standard]

# Using uv (recommended)
uv add fastapi uvicorn[standard]
```

## Core Concepts

### 1. FastAPI Instance
```python
from fastapi import FastAPI

app = FastAPI()
```
- Creates the main application instance
- This is the entry point for your API
- Can be configured with metadata, title, version, etc.

### 2. Path Operations (Route Decorators)
FastAPI uses decorators to define API endpoints:
- `@app.get()` - HTTP GET requests
- `@app.post()` - HTTP POST requests
- `@app.put()` - HTTP PUT requests
- `@app.delete()` - HTTP DELETE requests
- `@app.patch()` - HTTP PATCH requests

### 3. Path Parameters
The string inside the decorator defines the URL path:
- `@app.get('/')` - Root endpoint
- `@app.get('/hello')` - /hello endpoint
- `@app.get('/users/{user_id}')` - Dynamic path with parameter

## Code Analysis

### Current Implementation: `helloWorld.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {
        '/': 'list of the api endpoints',
        '/hello': 'here you get the response as Hello World'
    }

@app.get('/hello')
def hello_world():
    return {'message': 'Hello World'}
```

#### Technical Breakdown:

1. **Import Statement**
   ```python
   from fastapi import FastAPI
   ```
   - Imports the FastAPI class from the fastapi module
   - This is the core class for creating FastAPI applications

2. **Application Instance**
   ```python
   app = FastAPI()
   ```
   - Creates a FastAPI application instance
   - This instance will handle all incoming requests
   - Can be configured with parameters like title, description, version

3. **Root Endpoint (`/`)**
   ```python
   @app.get('/')
   def home():
       return {
           '/': 'list of the api endpoints',
           '/hello': 'here you get the response as Hello World'
       }
   ```
   - **Decorator**: `@app.get('/')` defines a GET endpoint at the root URL
   - **Function**: `home()` is the handler function
   - **Return**: Dictionary containing API documentation/endpoint list
   - **Purpose**: Serves as an API index or documentation endpoint

4. **Hello World Endpoint (`/hello`)**
   ```python
   @app.get('/hello')
   def hello_world():
       return {'message': 'Hello World'}
   ```
   - **Decorator**: `@app.get('/hello')` defines a GET endpoint at `/hello`
   - **Function**: `hello_world()` is the handler function
   - **Return**: JSON response with a message key
   - **Purpose**: Simple endpoint returning a greeting message

## API Endpoints

### Current Endpoints:

1. **GET /** (Root)
   - **Purpose**: API documentation/index
   - **Response**: JSON object listing available endpoints
   - **Use Case**: API discovery and documentation

2. **GET /hello**
   - **Purpose**: Hello World endpoint
   - **Response**: JSON with message field
   - **Use Case**: Basic endpoint testing and validation

### Expected API Behavior:
```json
// GET /
{
    "/": "list of the api endpoints",
    "/hello": "here you get the response as Hello World"
}

// GET /hello
{
    "message": "Hello World"
}
```

## Best Practices

### 1. Function Naming
- Use descriptive function names: `home()`, `hello_world()`
- Follow Python naming conventions (snake_case)
- Make function names reflect their purpose

### 2. Response Structure
- Return consistent data structures
- Use meaningful key names in dictionaries
- Consider using Pydantic models for complex responses

### 3. Endpoint Design
- Root endpoint (`/`) should provide API overview
- Use clear, RESTful URL patterns
- Include proper HTTP status codes (FastAPI handles this automatically)

### 4. Code Organization
- Keep imports at the top
- Group related endpoints together
- Add comments for complex logic

## Running the Application

### Method 1: Using uvicorn directly
```bash
uvicorn practice_files.helloWorld:app --reload
```

### Method 2: Using Python module
```bash
python -m uvicorn practice_files.helloWorld:app --reload
```

### Method 3: Using uv
```bash
uv run uvicorn practice_files.helloWorld:app --reload
```

### Parameters Explained:
- `practice_files.helloWorld:app` - Module path and app instance
- `--reload` - Auto-reload on code changes (development only)
- `--host 0.0.0.0` - Bind to all interfaces (optional)
- `--port 8000` - Port number (default: 8000)

### Accessing the API:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Next Steps for Learning

1. **Add More HTTP Methods**: Implement POST, PUT, DELETE endpoints
2. **Path Parameters**: Add dynamic URL parameters
3. **Query Parameters**: Handle URL query strings
4. **Request Body**: Process JSON request data
5. **Pydantic Models**: Define data validation schemas
6. **Database Integration**: Connect to databases
7. **Authentication**: Implement user authentication
8. **Error Handling**: Add proper error responses
9. **Testing**: Write unit tests for endpoints
10. **Deployment**: Deploy to production servers

## Common Issues and Solutions

### 1. Import Errors
- Ensure FastAPI is installed: `pip install fastapi`
- Check Python environment and virtual environment

### 2. Port Already in Use
- Change port: `uvicorn app:app --port 8001`
- Kill existing process using the port

### 3. Module Not Found
- Ensure correct module path in uvicorn command
- Check file structure and imports

### 4. Auto-reload Not Working
- Ensure `--reload` flag is used
- Check file permissions and IDE settings

## Resources
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [CampusX YouTube Channel](https://www.youtube.com/@CampusX-official)
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)
- [Uvicorn Documentation](https://www.uvicorn.org/)
