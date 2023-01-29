---
files: [app.py]
window: [terminal]
---

# Final Project : ShuttleShare

I implemented a website where University of Notre Dame students can find other students planning similar rideshares at similar times.

## Background

The University of Notre Dame hosts a diverse student body from across the country and global. 87% are from outside the Midwest and 12% are from outside the U.S. Since Notre Dame is located in South Bend, Indiana, this presents a logistical challenge when it comes to traveling to and from campus. Students in the Midwest typically opt to drive, but the majority of students are forced to use air travel. South Bend does have a local airport, but due to the lack of incoming flights, most students who fly choose to fly into Chicago, at either O'Hare or Midway. From there, they can take a train into Downtown Chicago, a train from Chicago to South Bend, then call a ride from the train station to Campus.

Since that route takes up to 5-7 hours, many students choose to bite the bullet take an expensive ($200) 2-hour Uber from the Chicago airports to Notre Dame campus. Given the high cost, many students reach out to large groupchats to coordinate rides with students taking similar trips.

ShuttleShare is a solution to this logistical challenge. It offers students the ability to find other students taking similar rides at similar times as they are. Students can "join" rides, unless the ride is full. They can view their historical or upcoming planned trips, as well as the email addresses of the other riders.


### Configuring

There are no configuration tasks to be done in order to run this application, other than setting up an active CS50 codespace.

### Running

Start Flask's built-in web server (within `final/`):

```
$ flask run
```

Once you have the generated URL, click it and you will be redirected to the login page. If you are visiting this site for the first time, please register a new user by clicking the "Register" tab at the top of the screen.

To register a user, please enter an email address in a valid format (this email will not be verified). This will be used as your username.


## Testing

#### User Login/Registration

* Creating a new user through the registration screen
* Logging in as a user and navigating to the "Plan your Trip" tab

#### Search

* Searching for rides for time ranges where there is data (O'Hare to Notre Dame on December 8th & 18th, 2022 should have a lot of data)
* For rides with departure dates in the past, you should not be able to join (the button should be disabled)
* For rides at capacity, you should also not be able to join
* If you attempt to join a ride you're already a member of, you should get an error
* If you attempt to join a valid ride (in the future/ under capacity/ not currently a member of), you should get a success confirmation screen and that ride should now appear on your "My Trips" page

#### Create

* Create your own ride by going first to the "Plan Your Trip" tab, then choose the create option
* All fields should be required
* If you select the starting location and destination as the same place, you should experience an error screen
* if you select a date in the past, you should experience an error screen
* If you create a valid ride, you should be automatically be added as a member. It should show up in your "My Trips" page, and it should be discoverable by users in the search page.

#### My Trips
* After joining trips by creating them or through the join option on the search page, you should see the trip details listed on this page upon initialization.
* For each rider in the trip, you should see their email address listed in the riders column for that row.
* To cancel a trip, select the cancel button on any of the trips. You should be taken to a confirmation screen notifying you of a successful cancellation and this ride should no longer appear in your "My Trips" page. If you were the only rider in this trip, the trip itself should be deleted, so that no rider-less trips are listed in the search results page.

## Video Demo
{% video https://youtu.be/jggU88oa604 %}