# Fourth Milestone Project

This project is heavily based on cars. Being this is a passion of mine I wanted to implement this in my project and came up with the idea of a website that stores vehicles which has information including who uploaded it, this includes the ability to add an image. If browsing as another use who hasn't uploaded the particular vehicle they can view the vehicle in more detail and also give the car a 'like'. There's a summary page which collects data from a JSON URL and puts itself into a dynamic chart and table.

# UX

My UX process was to analyze the customer’s requirements and try and think of different ways to implement this in an easy manner for the user.

## The client’s requirements are:

    To be able to register and sign into an account
    To be able to create, edit, delete and view vehicles on their account
    To be able to up vote and down vote on vehicles of other users (including their own)
    To be able to view vote scores
    To be able to see certain statistics of what's in the database

## User stories:

    As a user I want to be able to create an account
    As a user I want to be able to create, edit and delete vehicles
    As a user I want to view other user’s vehicles
    As a user I want to be able to vote on other user’s vehicles
    As a user I want be able to see a vehicles likes
    As a user I want to see if I have already voted on a vehicle
    As a user I want to be able to log out of my account

Important UX Notes

The way my authentication works is with a global variable that holds the username and stores it in a session. If this session expires then the application hits an exception and users are redirected back to the login screen.

In my app I have exceptions that catch all. This isn't best practice and is something I'd like to work on in the future but I do have alternative routes for all the errors that can happen so it's smooth for the user.

## Front End Design

Login/Register Pages - These pages use the same design. If the user has an issue with either login or registration then a information message should appear on the screen.

Home Page - The home page appears to all users who have just logged in. This page explains how the site works and also shortcuts to the filter and summary pages.

Search Database - This page displays all the vehicles in the database. You have the ability to filter by Region and/or Drive type as well as order by Brand name (A - Z) or vehicles who have likes on them.

Summary - This page allows the user to select a few criteria's on a drop down to display information with the vehicles in the database which is then pushed onto a bar chart as well as in a table which will display some extra information.

New Vehicle - This page allows the user to fill out information for the vehicle they're wanting to add to the database, add an image and a description either about the car or what they've done to it.

More Info - This is a route off the search database page where when a user finds a car displayed that they would like more info on, they click the 'More Info' button which then brings up a page with just that one vehicle.

Edit Vehicles - This is accessed once the user has gone into 'More Info' and confirms they're the user that uploaded that vehicle. They'll be a button which will then allow them to edit any bit of information about that vehicle, including adding a new image.

Delete Vehicle - THis is also accessed via the 'more info' page and confirms that the only person who can delete the selected vehicle is the user that uploaded it. 

## Backend

My backend consists of a relatively simple MySQL database. For testing and Development I use the local Cloud 9 Database and then for the live version I use the ClearDB heroku add on.

My Database consists of 4 tables:

    users
    cars
    popularity

The ER Diagram for my database:

.:: Attached as image in repositry ::.


# Features

The features of this application are as follows:

    Ability to Register, Sign into and Logout of an Account
    Ability to Create, Edit, Delete and View Vehicles
    Ability to vote on vehicles
    Ability to see if voted on a vehicle and to view its total likes
    Ability to order by Brand, Drive type and organise by Brand name (A - Z) or if the vehicle has likes

Features Left to Implement

I'd like to implement a personal profile to have user upload vehicles to their own 'garage'. From this, with enough information I could start implementing average stats, or who has the fastest car of this type,

With the personal profile implementation above I'd like to make a section of the site to allow users to find local 'meets' or even make new friends being able to find out who lives nearby. 

Ability to be able to search would be a nice benefit both Vehicles and Profiles (once added).

# Technologies Used

Python, Flask, werkzeug, JSON, WTForms, d3 and SQLAlchemy

Flask is the Python Framework I’m using for this application. 

Werkzueg - I've used  for securing image uploads to make sure no one uploads any old document and also to stop users intercepting it. 

JSON - I've used this to transmit my array over URL to be used in the graphs.js file creating a chart and table. 

WTForms - I've used this to create my forms, works well in conjunction with SQLAlchemy.

d3 - Used to create my bar charts.

SQLAlchemy - This is the module used for all my database queries/commits.

## CSS

I'm using SCSS to build my css style sheet which has SASS doing the conversion for me.

## JQuery

I've used JQuery to do a simple 'back to top' function but also to convert and display my data into d3 which is used to convert my data into a visible chart and table. 

## Testing

For testing I have tried the following browsers; Firefox, Chrome, Edge and Internet Explorer.

I've used my PC at home which uses the screen size 2560 x 1080 and built in reponsive browser feature mainly in firefox to test for different resolutions/devices.

## Testing Scenarios

    Try registering a user that already exists on the system
    Register a new user
    Login with incorrect details
    Login in with correct details
    Create a new vehicle
    Edit a vehicle
    Delete a vehicle
    Vote Up a vehicle
    Vote Down a vehicle
    Filter vehicles by Region
    Filter vehicles by Drive type
    Filter vehicles by Drive type and Region
    Order vehicles by Brand (A - Z)
    Order vehicles by Liked
    Order vehicles by Brand (A - Z) with the previous filtering tests
    Order vehicles by Liked with the previous filtering tests
    Edit a vehicle using the URL and vehicle id for a vehicle that has matching upload_by and current user
    Edit a vehicle using the URL and vehicle id for a vehicle that is another user’s upload
    Delete a vehicle using the URL and vehicle id for a vehicle that has the matching upload_by and current user
    Delete a vehicle using the URL and vehicle id for a vehicle that is another user’s vehicle
    Logout

# Deployment

While developing this app, my code was written in Cloud 9 and then migrated across to AWS Cloud 9. Throughout the development I used GitHub to keep track of changes.

The development version of my application is on GitHub and I push this code using git push origin master.

I've done all my testing on a local database which doesn't get uploaded to GitHub.

## Heroku Deployment Steps

    Go to the Heroku Website and create new app
    Create requirements.txt and Procfile to tell heroku what is required to run the app
    Login into Heroku Account via command line and add the newly created app
    Go back to Heroku Website and in the settings tab click Reveal Config Vars and add IP and PORT vars from Project Config
    Install ClearDB and import local MySQL Database dump.sql
    Restart all dynos
    Last but not least, do an initial git commit and push to heroku

# Acknowledgements

    Pencil - To draw my mock ups.
    ClearDB - Database hosted on Heroku/
    SQL image
