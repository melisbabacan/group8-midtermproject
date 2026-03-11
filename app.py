from flask import Flask
import psycopg2
 
app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="cities",
        user="postgres",
        password="password"
    )
 
@app.route("/hello")

def hello():

    return "Hello! Welcome to Favorite City App"
 
if __name__ == "__main__":

    app.run(debug=True)
 