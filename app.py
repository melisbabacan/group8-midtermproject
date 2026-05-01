from flask import Flask, jsonify
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_NAME = "group8kv"
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

favorite_cities = []


def get_db_secrets():
    """
    Lazily load DB secrets from Key Vault using Managed Identity.
    This keeps non-DB endpoints working even if Key Vault/DB is unavailable.
    """
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

    return {
        "host": secret_client.get_secret("DB-HOST").value,
        "name": secret_client.get_secret("DB-NAME").value,
        "user": secret_client.get_secret("DB-USER").value,
        "password": secret_client.get_secret("DB-PASSWORD").value,
    }


def get_connection():
    secrets = get_db_secrets()
    return psycopg2.connect(
        host=secrets["host"],
        database=secrets["name"],
        user=secrets["user"],
        password=secrets["password"],
        port=5432,
        sslmode="require",
    )

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


@app.route("/db-test")
def db_test():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify({"status": "success", "message": "PostgreSQL connection is successful."}), 200
    except Exception as exc:
        return jsonify({"status": "failure", "message": f"PostgreSQL connection failed: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)