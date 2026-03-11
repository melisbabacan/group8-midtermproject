from flask import Flask
import os
import psycopg2
 
app = Flask(__name__)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
 
@app.route("/hello")

def hello():

    return "Hello! Welcome to Favorite City App"
 
if __name__ == "__main__":

    app.run(debug=True)
 