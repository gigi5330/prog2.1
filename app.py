from flask import Flask, render_template, request, redirect, send_from_directory
from jinja2 import Environment, PackageLoader, FileSystemLoader
import json
from datetime import datetime
import os

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

# Erstelle data.json falls nicht vorhanden


def read_json_data(file_name="data.json"):
    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
        return data
    except:
        return None

# speichere Transaktion in data.json


def write_transaction(transaction):
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)
    json_data["transactions"].append(transaction)
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

# speichere Kategorie in data.json


def write_category(category):
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)
    json_data["categories"].append(category)
    with open("data.json", "w") as json_file:
        json.dump(json_data, json_file)

# speichere Budget in data.json


def write_budget(budget):
    with open("data.json", "r") as json_file:
        loaded_data = json.load(json_file)
        loaded_data["budget"] = budget
    with open("data.json", "w") as json_file:
        json.dump(loaded_data, json_file)

# Berechne verbleibendes Budget


def calculate_budget_remaining(data):
    budget = data["budget"]
    transactions = data["transactions"]
    bilanz_transactions = 0
    for transaction in transactions:
        bilanz_transactions += transaction["amount"]
    return budget + bilanz_transactions

# Datenübergabe an index.html


@app.route("/", methods=["GET", "POST"])
def index():
    data = json.loads(open("data.json").read())
    budget_remaining = calculate_budget_remaining(data)
    return render_template("index.html",
                           categories=data["categories"],
                           budget_remaining=budget_remaining,
                           transactions=data["transactions"],
                           budget=data["budget"])

# Budget setzen


@app.route("/set-budget", methods=["POST"])
def set_budget():
    budget = int(request.form["budget-amount"])
    write_budget(budget)
    return redirect("/")

# Transaktion Einkommen hinzufügen


@app.route("/add-income", methods=["POST"])
def add_income():
    current_time = datetime.now().strftime("%Y-%m-%d")
    new_transaction = {
        "title": request.form["transaction-title"],
        "amount": int(request.form["transaction-amount"]),
        "category": request.form["category"],
        "date": current_time
    }
    write_transaction(new_transaction)
    return redirect("/")

# Transaktion Ausgabe hinzufügen


@app.route("/add-expense", methods=["POST"])
def add_expense():
    current_time = datetime.now().strftime("%Y-%m-%d")
    new_transaction = {
        "title": request.form["transaction-title"],
        "amount": int(request.form["transaction-amount"]),
        "category": request.form["category"],
        "date": current_time
    }
    if new_transaction["amount"] > 0:
        new_transaction["amount"] = new_transaction["amount"] * -1
    write_transaction(new_transaction)
    return redirect("/")

# Kategorie hinzufügen


@app.route("/add-category", methods=["POST"])
def add_category():
    new_category = request.form["new_category"]
    write_category(new_category)
    return redirect("/")

# Einbindung static elemente


@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run(debug=True)
