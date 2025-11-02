from flask import render_template,request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from main_app import Main
from data_base import db, User_info,app, User
import secrets

main = Main()
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/FlightFind/<username>', methods = ["GET","POST"])
def ui(username):
    user = User.query.filter_by(username=username).first()
    if request.method == "POST":
        cities = [request.form["from_country"], request.form["to_country"]]
        city_codes = main.iata_find(cities)
        user = User.query.filter_by(username=username).first()
        print(user.username)

        data = User_info(
            user_name = user.username,
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            from_country = request.form["from_country"],
            to_country = request.form["to_country"],
            travel_date = request.form["travel_date"].replace("/","-"),
            depature_date = request.form["depature_date"].replace("/","-"),
            nonstop = request.form.get("nonstop"),
            from_iata= city_codes[0],
            to_iata= city_codes[1],
            price = request.form["max_price"]
        )
        db.session.add(data)
        db.session.commit()

        user_info  = User_info.query.filter_by(user_name=username).first()

        if user_info.nonstop and len(user_info.price) > 2:
            flight_data = main.flight_find(username, user_info.nonstop,cities)

            if not flight_data.nonstop_found:
                return render_template("flight_ui.html", nostop=False, user=user, price=True, message="No nonstop flights found. Showing flights with stops.")   

            return redirect(url_for('prices', username=user.username, price=float(user_info.price) ))
        else:
            print("ran")
            return render_template("flight_ui.html", user=user, nostop=False, price = False)
    
    return render_template("flight_ui.html", nostop=True, user=user)

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        confirm_password = request.form["confirm_password"]
        
        if request.form["password"] != confirm_password:
            flash("❌ Passwords do not match. Please try again.", "danger")
            return redirect(url_for("signup"))
        hashed_pw = generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=16)
        user_info = User(
            username = request.form["username"],
            email = request.form["email"],
            password = hashed_pw
        )

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email = email).first()

        if existing_email:
            flash("❌ Email already registered. Try logging in instead.", "danger")
            return redirect(url_for("signup"))

        if existing_user:
            flash("❌ Username already taken. Please choose another one.", "danger")
            return redirect(url_for("signup"))

        try:
            db.session.add(user_info)
            db.session.commit()
            flash("✅ Account created successfully! You can now log in.", "success")
            return redirect(url_for("login"))
        
        except:
            print("Couldn't record user info")
        
    return render_template("signup.html")

@app.route("/login", methods= ["GET", "POST"])
def login():
    if request.method == "POST":
        info = request.form["info"]
        user = User.query.filter((User.email==info) | (User.username==info)).first()

        if check_password_hash(user.password, request.form["password"]):
            return redirect(url_for('ui', username=user.username))
        else:
            flash("❌ Invalid credentials. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/pricing/<username>/<price>')
def prices(username, price):
    user = User.query.filter_by(username=username).first()
    
    price_float = float(price)
    print(f"{price_float} : {type(price_float)}")
    cons = main.get_flight_data()
    contents = main.pricing(cons, price_float)
    if contents:
        prices = [price["price"] for price in contents]
        flights = [deats["data"] for deats in contents]
        data = {key:value for key,value in enumerate(flights)}

        try:
            return render_template("prices.html", data= True, details=contents, prices=prices, flights=data, user=user)
        except:
            return render_template("prices.html", data= False, message = "ERROR")
    
    return render_template("prices.html", data= False, message = "❌ No flights found within your specified price range.")
