# Fourth Milestone Project

This project is heavily based on cars. Being this is a passion of mine I wanted to implement this in my project and came up with the idea of a website that stores vehicles for others to view and give a 'like'. You can filter through the list of vehicles and click on the 'more info' button which will bring up all the information for that vehicle on a new page. If you are the user that uploaded this vehicle you can edit or delete it from the database. There's a summary page which collects certain data from a dropdown menu which will send it via a JSON URL and put itself into a dynamic chart and table to make it easy to read.

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

My backend consists of a relatively simple MySQL database. For testing and Development I use the local Cloud 9 Database and then for the live version I use the Postgres heroku add on.

My Database consists of 3 tables:

    Users
    Cars
    Popularity

The ER Diagram for my database:

.:: Attached as image in repositry ::.

# Features

The features of this application are as follows:

    Ability to Register, Sign into and Logout of an Account
    Ability to Create, Edit, Delete and View Vehicles
    Ability to vote on vehicles
    Ability to see if voted on a vehicle and to view its total likes
    Ability to order by Brand, Drive type and organise by Brand name with an assortment of filters

## Features Left to Implement

I'd like to implement a personal profile to have user upload vehicles to their own 'garage'. From this, with enough information I could start implementing stats for that users vehicles or a % of likes with the same vehicle uploaded by others.

With the personal profile implementation above I'd like to make a section of the site to allow users to find local 'meets' or even make new friends being able to find out who lives nearby, thus also implementing a 'friends' system in. 

Ability to be able to search would be a nice benefit both Vehicles and Profiles (once added).

# Technologies Used

Python, Flask, werkzeug, JSON, WTForms, d3 and SQLAlchemy

Flask is the Python Framework I’m using for this application. 

Werkzueg - I've used  for securing image uploads to make sure no one uploads any old document and also to stop users intercepting it. 

JSON - I've used this to transmit my array over URL to be used in the graphs.js file creating a chart and table. 

WTForms - I've used this to create my forms, works well in conjunction with SQLAlchemy.

d3 - Used to create my bar charts.

SQLAlchemy - This is the module used for all my database queries/commits.

Boto3 / S3 - Used for uploading images to my Bucket hosted on AWS. 

## CSS

I'm using SCSS to build my css style sheet which has SASS doing the conversion for me.

Animated CSS by Daniel Eden. I love this package and use it with all my projects, if needed it can be amended with javascript to make it run a function when it's finished animating and much more (link below).

## JQuery

I've used JQuery to do a simple 'back to top' function but also to convert and display my data into d3 which is used to convert my data into a visible chart and table. 

## Testing

For testing I have tried the following browsers; Firefox, Chrome, Edge and Internet Explorer.

I've used my PC at home which uses the screen size 2560 x 1080 and at work which is dual screen setup, used the built in "reponsive browser" feature mainly in firefox to test for different resolutions/devices.

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
    Order vehicles by Horsepower (High to Low) with previous filtering tests
    Order vehicles by Horsepower (Low to High) with previous filtering tests
    Edit a vehicle using the URL and vehicle id for a vehicle that has matching upload_by and current user
    Edit a vehicle using the URL and vehicle id for a vehicle that is another user’s upload
    Delete a vehicle using the URL and vehicle id for a vehicle that has the matching upload_by and current user
    Delete a vehicle using the URL and vehicle id for a vehicle that is another user’s vehicle
    Logout

## Bugs

Filter-page: When the user wants to search by 'Likes', this brings back the results but not in order, however, if you keep it on 'Likes' and add the Region to be 'JDM' it orders the results correctly even though it's displaying the same vehicles on my testing, likewise with different regions or transmission types. I've had a tutor try and look into this with me but after a week with no results I've added this to the bugs unfixed list.

Vehicle Images: When I moved my image storage over to S3 Bucket from the local list, when you went through and reuploaded the same image to update the file path to it's location it update but not display the image. This was because the bucket policy wasn't setting the uploaded content to be 'Public' even though I had set the bucket to be. Tutor helped with this by placing a bucket policy to set newly added documents to be public/read by all.

S3 Bucket: After fighting with this for a little while tutors have mentioned i couldn't create a User needed to gain an access and secret key for my app to upload to my bucket. Have created a new free account in AWS, setup the new bucket and now have a user with needed information. Previously I could upload with no issues within AWS cloud9 but when running from Heroku it would say it had uploaded the image when it hadn't, confirmed looking by looking in the bucket for the image to not be there.

# Deployment

While developing this app, my code was written in Cloud 9 and then migrated across to AWS Cloud 9. Throughout the development I used GitHub to keep track of changes.

The development version of my application is on GitHub and I push this code using git push origin master.

I've done all my testing on a local database which doesn't get uploaded to GitHub.

## Heroku Deployment Steps

    Go to the Heroku Website and create new app
    Create requirements.txt and Procfile to tell heroku what is required to run the app
    Login into Heroku Account via command line and add the newly created app
    Go back to Heroku Website and in the settings tab click Reveal Config Vars and add IP and PORT vars from Project Config
    Install PostGres and run my models.py to create my database.
    Restart all dynos
    Last but not least, do an initial git commit and push to heroku
    
    **Since moving over to AWS Cloud9 my heroku commands don't want to work so I now deploy via the 
    option on heroku which if you have it linked to your GitHub, it'll download/clone the files across
    for you.

## Live Version of the App

https://fourth-milestone-carpedia.herokuapp.com/

# Acknowledgements

    Pencil - To draw my mock ups.
    Animated.css - https://daneden.github.io/animate.css/
    Postgres - Database hosted on Heroku
    SQL Schema - dbdiagram.io
    SQLAlchemy - Google/FullStack search results using snippets and amending for my purpose
    Images - Google Images
    CI Tutor - Helped with implementing my S3 Bucket storage and setting newly added documents to be public
