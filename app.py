from flask import Flask, jsonify
 
app = Flask(__name__)
 
favorite_cities = []
 
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
    app.run(debug=True)