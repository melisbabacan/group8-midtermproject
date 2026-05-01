from flask import Flask, jsonify
import psycopg2

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
app = Flask(__name__)
 
KEY_VAULT_NAME = "group8kv"
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

credential = DefaultAzureCredential()
secret_client = SecretClient(
    vault_url=KEY_VAULT_URL,
    credential=credential
)

DB_HOST = secret_client.get_secret("DB-HOST").value
DB_NAME = secret_client.get_secret("DB-NAME").value
DB_USER = secret_client.get_secret("DB-USER").value
DB_PASSWORD = secret_client.get_secret("DB-PASSWORD").value

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=5432,
        sslmode="require"
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