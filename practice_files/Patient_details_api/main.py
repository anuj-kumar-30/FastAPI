from fastapi import FastAPI, Path, HTTPException, Query
import json 

# creating instance of FastAPI, to access the HTTP method and api endpoints
app = FastAPI()

# all the helper function
# 1. load patient json file -> json data
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

## 1. Create an api endpoint to show the list of all the endpoints as well as it's discription
@app.get('/')
def home():
    return {
        "message": "Welcome to Patient Details API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": {
                "description": "Get list of all available endpoints",
                "example": "GET /"
            },
            "GET /patient": {
                "description": "Get list of all patients details",
                "example": "GET /patient"
            },
            "GET /patient/{patient_id}": {
                "description": "Get details of a specific patient by ID",
                "example": "GET /patient/P001",
                "parameters": {
                    "patient_id": "Patient ID (e.g., P001, P002)"
                }
            },
            "GET /sort": {
                "description": "Sort patients by height, weight, or BMI",
                "example": "GET /sort?sort_by=height&order=asc",
                "query_parameters": {
                    "sort_by": "Field to sort by (height, weight, bmi)",
                    "order": "Sort order (asc, desc) - default: asc"
                }
            }
        },
        "usage": {
            "get_all_patients": "GET /patient",
            "get_specific_patient": "GET /patient/P001",
            "sort_patients_by_height": "GET /sort?sort_by=height&order=asc",
            "sort_patients_by_weight_desc": "GET /sort?sort_by=weight&order=desc"
        }
    }

@app.get('/patient')
def view_patients():
    # first load all the patient data
    data = load_data()
    return data

## 2. Create an endpoint where we will get the details for the specific patient based on their id
# - to achieve above aim, we will be using path parameters
# - Path parameters: They are dynamic segment of the url eg: localhost:8000/patient/{patient_id}
# - These path parameters are mainly used to locate some specific resources. in our case patient details

# @app.get('/patient/{patient_id}') # here patient_id is a path parameters
# def view_specific_patient(patient_id: str): # here we are passing same patient we get from the url
#     data = load_data() 
#     if patient_id in data: # checking if the patient is present or not 
#         return data[patient_id]
#     return {'error':'Patient Not Found'}

# Let's make some improvement in our above code's limitations
# Limitations:
# 1. the path params is not descriptive, means just looking the path params we can't get what kind of input it is taking
# - to overcome this we can add some example input as well as we can add a discription for that path params 
# - to achieve this we will using Path() method from fastapi 
## This method in FastAPI is used to provide metadata, validation rules, and documentation hints for path parameters in our API endpoints
## parameters of path method
# - title
# - Description
# - Example
# - ge, gt, le, lt
# - Min_length
# - Max_length
# - regex

### Imporved code
@app.get('/patient/{patient_id}') # here patient_id is a path parameters
def view_specific_patient(patient_id: str = Path(..., description = "ID of a patient in the DB", example = 'P001')): # here we are passing same patient we get from the url
    data = load_data() 
    if patient_id in data: # checking if the patient is present or not 
        return data[patient_id]
    # return {'error':'Patient Not Found'} # problem show 200 status code which is not right
    raise HTTPException(
        status_code=404,
        detail="Patient Not Found"
    ) # with we are raising with 404 status code: which represent resouce not found, and we are also providing detail what kind of error it is
# str = Path(..., description = "ID of a patient in the DB", example = 'P001')
# ... -> required parameter

## let's apply sorting function to our pateint details endpoint
# - to achieve this we will be using query parameter
# - the query parameter endpoint look something like this: /patient?city=Delhi&sort_by=age
# - Now in our case we want to apply the sorting based on feature name and order
# - it will have two query: 
#   - sortby=ht/wt/bmi
#   - order=asc/desc 
# - both of the query can be optional
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="Sort the values based on height, weight, BMI, etc"), order: str = Query('asc', description="sorting type asc or desc")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Given input is not correct select from this {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Given input for sort order is not valid valid data = {['asc', 'desc']}")
    
    data = load_data()
    sorted_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order)
    return sorted_data