#q25 FASTAPI

#note sice there is no DB the student we create or update will not persist across server restarts, as we are using a simple dict to store student data in memory only., it will persist only during the server runtime.

#instead of using Flask, we are using FastAPI for better performance and async support
from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel
#uv add pydantic

app = FastAPI()

@app.get("/")
def home():
 return { "message": "Hello TDS!"}

students={
   1: {"name": "Alice", "age": 21,"class_name": "year 12" },
}

#Pydantic model for student ie, it acts as a schema/structure for student data validation
class Student(BaseModel):
    name: str
    age: int
    class_name: str

#Pydantic model for updating student ie, all fields are optional here
#coz in update we may not want to update all fields
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_name: Optional[str] = None


#@app.route("/student/<int:student_id>")  # Flask style
#def get_student(student_id):
#    return students.get(student_id, {"error": "Student not found"})

@app.get("/student/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student to retrieve", gt=0,lt=3)):   
    return students.get(student_id, {"error": "Student not found"})
#or return student[student_id]  will give keyerror if id not found
#Path is used to add extra validation and description to the path parameter student_id, like gt=0 means greater than 0, you can add lt,ge,le etc for validation
#check swagger docs at http://127.0.0.0:8000/docs for more info


#QUERY PARAMS
# @app.get("/get-by-name")
# # def get_student_by_name(name: str=None):
# def get_student_by_name(test: int, name:Optional[str]=None):
#     for student_id in students:
#         if students[student_id]["name"] == name:
#             return students[student_id]
#     return {"error": "Student not found"}

#str=None means its(query param) optional, if not provided it will be None(otherwise it will be a required query param in swagger ui docs)
#Optional imported from typing module is used to indicate that the parameter can be of type str or None, it is more explicit and helps with type checking.
#note test is a required query param here as no default value is given. and it must come before the optional params. coz parms with default values come last.
#or can do 
# def get_student_by_name(*,name: Optional[str] = None, test: int):

# use the below one ie run uv run myapi.py  (python3 myapi.py wont work directly as uvicorn is needed to run fastapi apps, and it is installed in the uv environment only)
#  or can run directly in terminal with: uv run uvicorn myapi:app --reload --host 127.0.0.1 --port 8000

#COMBINING PATH AND QUERY PARAMS
@app.get("/get-by-name/{student_id}")
def get_student_by_name(*,student_id: int, name: Optional[str] = None,test:int):
    for id in students:
        if students[id]["name"] == name and id==student_id:
            return students[id]
    return {"error": "Student not found"}

#post method to create a new student
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    #post has a request body
    #the params in the above api function are taken from the request body automatically by FastAPI if they are of type Pydantic model, so here student param is taken from request body,student-id is taken from path(its a path param)
    # so student param will have the data sent in the request body as json
    if student_id in students:
        return {"error": "Student already exists"}
    #practically i think instead of a simple dict we can use a database to store student data, so here we are simulating that with a simple dict
    #if a db, then here it would be - student_obj=StudentModel(**student.dict())  # create a new student object from the Pydantic model data,and then
    # db_session.add(student_obj)
    # db_session.commit()

    students[student_id] = student
    return {"student":students[student_id],"message": "Student created successfully"}

# Yes, the Pydantic model is still needed even when using a database. Here's why:

# Request validation & parsing: FastAPI uses the Pydantic model to automatically validate and parse the incoming JSON request body. This happens at the API boundary before the data reaches your function.

# API documentation: The Pydantic model generates the Swagger/OpenAPI documentation showing clients what data structure to send.

# Separation of concerns: You typically have:

# Pydantic model (e.g., Student) - defines your API contract/request schema
# Database model (e.g., StudentModel) - defines how data is stored in the database
# So your code pattern would look like:

#PUT method to update existing student
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"error": "Student not found"}
    #practically i think instead of a simple dict we can use a database to store student data, so here we are simulating that with a simple dict
    #if a db, then here it would be - query the student from db first
    # student_obj = db_session.query(StudentModel).filter(StudentModel.id == student_id).
    # db_session.add(student_obj)
    # db_session.commit()

    #modify only the fields provided in the update request, others are kept intact
    if student.name is not None:
        students[student_id].name = student.name
    if student.age is not None:
        students[student_id].age = student.age
    if student.class_name is not None:
        students[student_id].class_name = student.class_name

    #instead of above if we just use students[student_id] = student , it will overwrite the entire student data with only the fields provided in the update request, and the fields not provided will be lost/nullified.
    return {"student":students[student_id],"message": "Student updated successfully"}


#DELETE method to delete a student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student not found"}
    #practically i think instead of a simple dict we can use a database to store student data, so here we are simulating that with a simple dict
    #if a db, then here it would be - query the student from db first
    # student_obj = db_session.query(StudentModel).filter(StudentModel.id == student_id).
    # db_session.delete(student_obj)
    # db_session.commit()

    del students[student_id]
    return {"message": "Student deleted successfully"}


























import uvicorn

if __name__ == "__main__":
    uvicorn.run(app,port=8000) # if host is 0.0.0.0 , then it will be accessible from outside the local machine, now its running only on localhost in wsl, which will be accessible by windows browser as well.
    #but if host="0.0.0.0", then it will be accessible from other devices in the same network as well(ie all wsl networks interfaces ) and from browser use http://<wsl_ip_address>:8000 (using 172.x.x ie real ip of wsl) or http://localhost:8000 (windows localhost forwarded to wsl localhost) 
    #dont use http://0.0.0.0:8000 in browser, it wont work.
    #read tds notes for more info

# same with flask

# from flask import Flask
# app = Flask(__name__)
# @app.route("/")
# def home_flask():
#     return { "message": "Hello TDS!"} #here this is a is a Python dictionary
#  Flask converts it into JSON (automatically) in the HTTP response, 
#to do it explicitly can use jsonify() function from flask return jsonify({"message": "Hello TDS!"})

# if __name__ == "__main__":   
#     app.run( port=8000) 

#Flask does not require uvicorn. running python3 myapi.py is enough to start the server...and flask is i guess globaly installed in wsl(by me)





