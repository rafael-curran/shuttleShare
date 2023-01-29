# this application is intended for students who want to split ubers from Chicago to Notre Dame campus

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from helpers import login_required

# Configure application
app = Flask(__name__)

# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shuttle.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#provisions the home page for ShuttleShare app
@app.route("/")
@login_required
def index():
    return render_template("index.html")

#for get request, provisions the login page
#for POST request, it intakes the username and password parameters and provisions a session if valid, or redirects the user to an error screen if not
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            message = "Username not submitted."
            return redirect(url_for('apology', message=message, code=403))

        # Ensure password was submitted
        elif not request.form.get("password"):
            message="Password not submitted."
            return redirect(url_for('apology', message=message, code=403))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect(url_for('apology', message="Invalid username and/or password", code=403))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#provisions the planning page when the user clicks on the "Plan a Trip" tab in the nav bar, which gives the user the option to find an existing trip or plan a new one
@app.route("/plan")
def plan():
    return render_template("plan.html")

#for GET requests, the create page is provided with a form to create a new ride
#for POST requests, the form values are used to insert a new ride into the Rides table
@app.route("/create", methods=["GET", "POST"])
def create():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #store form inputs into variable
        startLocName = request.form.get("starting")
        endLocName = request.form.get("destination")
        currentUser = session["user_id"]
        capacity = request.form.get("size")

        #check if startLoc is different then endloc. If it is the same, the user should be redirected to an error screen
        if(startLocName == endLocName):
            message = "Error: You cannot select the same starting location and destination."
            return redirect(url_for('apology', message=message))

        #to get the location names, I must execute SQL queries to return the name based on the location ID
        startloc = db.execute("SELECT id FROM locations WHERE name = ?",startLocName)[0]["id"]
        endloc = db.execute("SELECT id FROM locations WHERE name = ?",endLocName)[0]["id"]

        #since HTML and SQL format datetimes differently, I first convert it to a python datetime object then back to a string in the accepted SQL datetime format
        departime = request.form.get("departure-datetime")
        departTimeObj = datetime.strptime(departime, '%Y-%m-%dT%H:%M')
        departTime = departTimeObj.strftime('%Y-%m-%d %H:%M:%S')

        if departTimeObj < datetime.now():
            message = "Error: You cannot select departure dates in the past."
            return redirect(url_for('apology', message=message))




        #the rides record is inserted first, then the ID of the record is captured in the rideId variable so that the reference to the ride is maintained in the userrides table
        rideId = db.execute("INSERT INTO rides (owner_id, start_location_id, end_location_id, depart_date_time, capacity) VALUES(?, ?, ?, ?, ?)",
                       currentUser, startloc, endloc, departTime, capacity)

        #the userrides record, which essentially captures the RSVP of the user is inserted with the current user's id and the newly create ride id
        db.execute("INSERT INTO userrides (user_id, ride_id) VALUES (?, ?)", currentUser, rideId)

        #After the ride has been created, I redirect the user to the confirmation screen with the details of their newly created ride.
        message = "Your ride from " + startLocName + " to " + endLocName + " on " + departTime + " has been created."
        return render_template("confirmation.html", message=message)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("create.html")

#reachable by clicking the JOIN button on the search results page, this function adds the current user to the ride, if they are not a member already
@app.route("/join", methods=["POST"])
def join():
    # User reached route via POST (as by clicking the JOIN button which triggers a POST callout)
    currentUser = session["user_id"]
    rideId = request.form.get("rideid")
    #check if user already joined this ride
    rows = db.execute("SELECT id FROM userrides WHERE ride_id = ? AND user_id = ?", rideId, currentUser)

    #if user already joined, the above query will return a value. If so, the user should be redirected to an error notification
    if len(rows) != 0:
        message = "Error: You have already joined this ride. Please select another ride."
        return redirect(url_for('apology', message=message))

    #otherwise, proceed by inserting a new record into the userrides table
    db.execute("INSERT INTO userrides (user_id, ride_id) VALUES (?, ?)", currentUser, rideId)
    rideInfo = db.execute("SELECT rides.id, start_loc.name startloc, end_loc.name endloc, rides.depart_date_time departtime FROM rides INNER JOIN locations start_loc ON rides.start_location_id = start_loc.id INNER JOIN locations end_loc ON rides.end_location_id = end_loc.id WHERE rides.id = ?", rideId)[0]
    startLoc = rideInfo["startloc"]
    endLoc = rideInfo["endloc"]
    departtime = rideInfo["departtime"]
    message = "Your ride from " + startLoc + " to " + endLoc + " on " + departtime + " is confirmed"
    return redirect(url_for('confirmation', message=message))



@app.route("/search", methods=["GET", "POST"])
def search():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        startloc = request.form.get("startloc")
        endloc = request.form.get("endloc")
        departime = request.form.get("departime")
        datetime_object = datetime.strptime(departime, '%Y-%m-%dT%H:%M')
        rangestart = (datetime_object - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
        rangeend = (datetime_object + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')
        rows = db.execute("SELECT COUNT(userrides.id) current, start_loc.name startloc, end_loc.name endloc, rides.capacity cap, rides.depart_date_time departtime, rides.id rideid FROM userrides INNER JOIN rides ON userrides.ride_id = rides.id INNER JOIN locations start_loc ON rides.start_location_id = start_loc.id INNER JOIN locations end_loc ON rides.end_location_id = end_loc.id WHERE (departtime BETWEEN ? AND ?) AND end_loc.name = ? AND start_loc.name = ? GROUP BY rides.id ORDER BY departtime ASC", rangestart, rangeend, endloc, startloc)
        return rows
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("search.html")

@app.route("/mytrips", methods=["GET", "POST"])
def mytrips():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        currentUser = session["user_id"];
        rows = db.execute("SELECT COUNT(userrides.id) current, start_loc.name startloc, end_loc.name endloc, rides.capacity cap, rides.depart_date_time departtime, rides.id rideid FROM userrides INNER JOIN rides ON userrides.ride_id = rides.id INNER JOIN locations start_loc ON rides.start_location_id = start_loc.id INNER JOIN locations end_loc ON rides.end_location_id = end_loc.id INNER JOIN users ON users.id = userrides.user_id WHERE userrides.ride_id IN (SELECT userrides.ride_id FROM userrides WHERE userrides.user_id = ?) GROUP BY userrides.ride_id ORDER BY departtime ASC",currentUser)
        riderTable = db.execute("SELECT userrides.ride_id rideId, users.username username FROM userrides INNER JOIN rides ON userrides.ride_id = rides.id INNER JOIN users ON users.id = userrides.user_id WHERE userrides.ride_id IN (SELECT userrides.ride_id FROM userrides WHERE userrides.user_id = ?) ORDER BY rides.depart_date_time ASC", currentUser)
        #results is stored in a dict, so that I can use a key value pair of id -> ride and then add another array within the riders field
        results = {}
        for row in rows:
            row["riders"] = []
            results[row["rideid"]] = row
        #to render the riders for each ride within the table on mytrips, I add them to the riders column in the results object
        for rider in riderTable:
            results[rider["rideId"]]["riders"].append(rider["username"])

        return results
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("mytrips.html")

#given a ride id, this method deletes the userrides record from the db, effectively cancelling that user's RSVP to the ride
@app.route("/cancel", methods=["GET", "POST"])
def cancel():
    # User reached route via POST (as by clicking the cancel button that triggers a POST request)
    if request.method == "POST":
        rideId = request.form.get("rideId")
        currentUser = session["user_id"]
        #delete the userrides record from the db, which effectively cancels the user's RSVP
        id = db.execute("DELETE FROM userrides WHERE user_id = ? AND ride_id = ?", currentUser, rideId)

        #if there isn't a record deleted, show the error screen
        if(not(id)):
            message = "Something went wrong in your ride cancellation. Please try again."
            return redirect(url_for('apology', message=message))

        #check if there are any more remaining reservations by looking for other userrides records with this ride_id
        #if there are no more riders for this reservation, the ride should be cancelled (deleted)
        remaining = db.execute("SELECT COUNT(id) FROM userrides WHERE ride_id = ? GROUP BY ride_id", rideId)
        if(remaining == 0):
            db.execute("DELETE FROM rides WHERE ride_id = ?", rideId)

        message = "Your reservation has been cancelled."
        return redirect(url_for('confirmation', message=message))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        username = request.form.get("InputEmail")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # validating input to ensure that username, password, and confirmation
        if (username and password and (password == confirmation)):
            password = generate_password_hash(password)

            # attempt to add new user to the table, redirect to an apology page if this fails
            try:
                db.execute(
                    "INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
            except:
                message = "Error creating new user. Please try again."
                return redirect(url_for('apology', message=message))

            return render_template("login.html")
        else:
            message = "Error creating new user. Please ensure passwords match and try again."
            return redirect(url_for('apology', message=message))
    else:
        return render_template("register.html")

#routing location to display the confirmation screen with a given message
@app.route("/confirmation")
def confirmation():
    message = request.args.get('message')
    return render_template("confirmation.html", message=message)

#routing location to display the apology screen with a given message
@app.route("/apology")
def apology():
    message = request.args.get('message')
    return render_template("apology.html", message=message), 400
