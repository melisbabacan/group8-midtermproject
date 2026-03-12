from flask import Flask, jsonify
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
 
favorite_cities = []

@app.route("/")
def home(): 
    return "Favorite city app is running.."

@app.route("/hello")
def hello():
    return "Welcome to Favorite City App"
 
@app.route("/add/<city>")
def add_city(city):
    favorite_cities.append(city)
    return f"{city} added!"
 
@app.route("/cities")
def cities():
    return jsonify(favorite_cities)
 
@app.route("/delete/<city>")
def delete_city(city):
    if city in favorite_cities:
        favorite_cities.remove(city)
        return f"{city} deleted!"
    return "City not found"
 
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)