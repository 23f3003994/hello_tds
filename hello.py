#instead of using Flask, we are using FastAPI for better performance and async support
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def home():
 return { "message": "Hello TDS!"}
# use the below one ie run uv run hello.py  (python3 hello.py wont work directly as uvicorn is needed to run fastapi apps, and it is installed in the uv environment only)
#  or can run directly in terminal with: uv run uvicorn hello:app --reload --host 127.0.0.1 --port 8000
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

#Flask does not require uvicorn. running python3 hello.py is enough to start the server...and flask is i guess globaly installed in wsl(by me)



