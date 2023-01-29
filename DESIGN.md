---
files: [app.py]
window: [terminal]
---

# Final Project : ShuttleShare

### Design Overview

I chose to create a Flask Web-App due to my familiarity with the Flask framework from the CS50 Problem Sets. I also wanted to make this application more dynamic and responsive to the end-user, so I learned some JavaScript in order to fetch data from the Flask app and dynamically render many of the elements, especially on the search result page.  Since my data requirements were relatively straightforward, I chose to use a SQL database as well as CS50's SQL Python library to execute CRUD operations.

Although most of the validation in the problem sets was implemented in the server-side, I tried to implement some client side validation as well. On the create page, I used native HTML using required tags, but on the search page, I used the JavaScript Constraint Validation API's to ensure that all the values were filled in before attempting a search query.

Still, I implemented validation in the `app.py` functions as well, to ensure that many (but likely not all) erroneous actions are prevented. It should be impossible to have rides without riders. You shouldn't be able to join  or create rides in the past. You shouldn't be able to join the same ride twice.

### Contents

#### `app.py`

`app.py` contains the bulk of the back-end code for this Flask Application. This file reuses some of the code provided in the Finance problem set, namely the imports (SQL, flask, helper file), and login/register functions (with some modifications) but the majority of the code is original for this final project.

`index()` is the function called by the root route "/" and serves the index template.

`login()` is called by the route "/login" and accepts both GET and POST requests. When a user visits the URL route, they will be served a log in screen, where they can input their credentials. After submitting, the credentials are validated (by checking if they are blank) then the user table is queried via SQL to determine if the user exists. If the user exists, then the inputted password is processed through the hash function and the resulting hash value is compared against the hash value stored on the user record. If the hash values match, then the user is logged in, which entails that their user id is stored in the flask session variable and they are redirected to the home page.

`plan()` is called by the route "/plan" and accepts only GET requests. It renders the template for the plan page, which provides the user the option to either search and join an existing ride or create a new one.

`create()` is called by the route "/create" and accepts both GET and POST requests. When it receives a GET request, it renders the page for the ride creation page, which allows the user to input values for a new ride to be created. When the user submits that form, it sends a POST request which is then processed in this function by adding a new record to the rides table, using the provided values, then it adds a record to the userrides table to designate that that user will be a participant on that ride.

`join()` is called when the user selects the join button on the search results page. The rideId from the button element is passed in the body of the POST request, so this function checks if this user already joined this ride, and if they haven't, it inserts a new record into the userrides table for this user at this time.

`search()` accepts both GET and POST requests. GET requests simply renders the search.html page. POST requests are triggered by the form submission on the search.html page. Since it is unlikely that a user will find another ride for the exact time they are looking for, I have created a date range using python datetime objects, then converted them into strings for the SQL query so that they can be used in a BETWEEN clause. The resulting rides that match the query parameters are returned.


#### `helpers.py`

The only function I have kept in `helpers.py` is the login_required() decorator method which is used in `app.py` to designate routes which are only accessible to logged in users. If the user is not logged in, they are redirected to the login page.


#### `static/`

Of the three files in `static/`, one is an image used as the hero image of the homepage. It is sourced from [Wikipedia Commons](https://commons.wikimedia.org/wiki/File:Downtown_Chicago,_Illinois_%2814024062257%29.jpg)

The other two files are javascript files used for the search and mytrips pages.

`search.js` adds two important levels of functionality to the search page. Firstly, it adds an event listener to the form, which validates the inputted search arguments and then constructs a POST request to the /search endpoint. When the response is returned, it processes the data by creating a new table row for each ride that fits the query parameters. It uses a ternary operator to disable the join button if the ride is at capacity, preventing the user from joining a full ride.

Once the table is rendered (via DOM manipulation of the table element), it calls addJoinButtons() to add event listeners to all the join buttons. These event listeners listen for a click event, so when they are clicked, they construct a POST request to "/join" which creates a reservation for the specified ride (the ride id is stored in the value of the button element).

`mytrips.js` implements similar functionality, in terms of sending a POST request to query data, but no data is provided in the body of the request since the python endpoint only needs the user's id to filter the query. The table is constructed similarly to the table on the search page, except for instead of join buttons, the user is provided with cancel buttons. Pressing this button triggers a POST callout to the "/cancel" endpoint, which deletes the "userrides" or reservation record of that user for that ride.

#### `templates/`

`apology.html` is the template used for delivering error notifications. The message is inserted via a Jinja expression.

`confirmation.html` is the template used for delivering success confirmations for creating, joining or cancelling rides. Here, too, the message is inserted via a Jinja expression.

`create.html` is the template which contains the web form that allows users to create new rides. It contains fields for starting location, destination, departure time and an option for capacity of the rideshare they intend to call.

`index.html` is the home page for the application. It pulls in an image from the `/static` folder to be used as a hero image, then contains a link to the trip planning tab.

`layout.html` is the reused template which contains the non-main structure of the page, which includes the header/navigation bar and the footer. This template is reused on all other pages via the extension Jinja block.

`login.html` is the login page for this application. It is a simple form, with only a username and password field. Upon click of the submit button, the form's data is sent to the /login endpoint via post, and the user is either redirected to the home page (for successful logins) or an error screen for unsuccessful logins.

`mytrips.html` is the page which displays all of the current user's reservations, sorted chronologically with the latest first. It provides a list of all the riders' email addresses in the column, and even provides a cancel button if the user wishes to cancel their reservation.

`plan.html` is the landing page when the user clicks the nav tab to "Plan your Trip". Although users have the ability to search for existing rides, they might not find one and may choose instead to "Create a New Ride" in the hopes that future students may join their ride.

`register.html` is the user registration page for the site. The usernames are collected in the form of email addresses. The passwords inputted must also match, or the user will experience an error screen.

`search.html` is the page where users can search for and join existing rides. A form at the top of the page allows the user to input intended starting location, departure date/time, and destination. These are all required fields, and if you attempt to search without submitting all of them, you will experience error validation messages prompting you to fill them in. Once you input valid values and search, a list of rows should render in the table with details and a join option for each of the rides near that intended departure time. If there are no rides available then, you will see a message informing you so, with the suggestion to create a new ride, in the hopes that other students may join your ride.

