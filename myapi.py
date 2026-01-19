#q25 FASTAPI

#instead of using Flask, we are using FastAPI for better performance and async support
from fastapi import FastAPI,Path
from typing import Optional


app = FastAPI()

@app.get("/")
def home():
 return { "message": "Hello TDS!"}

students={
   1: {"name": "Alice", "age": 21,"class": "year 12" },
}


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
@app.get("/get-by-name")
# def get_student_by_name(name: str=None):
def get_student_by_name(test: int, name:Optional[str]=None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"error": "Student not found"}
#str=None means its(query param) optional, if not provided it will be None(otherwise it will be a required query param in swagger ui docs)
#Optional imported from typing module is used to indicate that the parameter can be of type str or None, it is more explicit and helps with type checking.
#note test is a required query param here as no default value is given. and it must come before the optional params. coz parms with default values come last.
#or can do 
# def get_student_by_name(*,name: Optional[str] = None, test: int):

# use the below one ie run uv run myapi.py  (python3 myapi.py wont work directly as uvicorn is needed to run fastapi apps, and it is installed in the uv environment only)
#  or can run directly in terminal with: uv run uvicorn myapi:app --reload --host 127.0.0.1 --port 8000
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





