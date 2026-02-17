# def main():
#     print("Hello from hello-tds!")

# #run python3 main.py in the terminal and see the output
# if __name__ == "__main__":
#     main()
import requests
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Dependabot demo project is working"}

# simple function using requests
def get_google():
    response = requests.get("https://www.google.com")
    return response.status_code

# simple pandas usage
def create_dataframe():
    data = {"name": ["Alice", "Bob"], "age": [25, 30]}
    df = pd.DataFrame(data)
    print(df)

if __name__ == "__main__":
    print("Google status:", get_google())
    create_dataframe()


