from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query

app=Flask(__name__)
app.secret_key="skrivnost123"

db=TinyDB("db.json")
users = db.table("users")

User = Query()

#homepage
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        if users.search(User.username==username):
            return "uporabnik ne obstaja"
        
        users.insert({"username":username, "password":password, "note": ""})
        return redirect("/login")
        #print(username, password)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        user = users.get(User.username=username)
        #print(user)
        if user in user["password"]==password:
            session["user"]=username
            return redirect("/dashboard")
        else :
            return "napačen login"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

app.run(debug=1)