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