# Kiwi

## About

Kiwi, like the bird not the fruit, is a webapp that keeps track of who has one common shared key. Users can use the app to indicate they have the key or returned it to a reception desk or lockbox.

## To run the development server do

~~~python
python3 manage.py runserver
~~~

## Make Tailwind update the css on changes

<https://tailwindcss.com/blog/standalone-cli>

## Windows

 ~~~ps1
./tailwindcss.exe -i 
keyTracker/static/keyTracker/css/input.css  -o keyTracker/static/keyTracker/css/output.css --watch
 ~~~

## Linux

 ~~~shell
./tailwindcss-linux -i keyTracker/static/keyTracker/css/input.css -o keyTracker/static/keyTracker/css/output.css --watch
 ~~~

# How it works

## sign up

When a user signs up, they enter a username, email, rnumber and password. They then need to be verified by the admin. The admin can do this by going to the django admin page and adding the newly created user to the group "DI". The user can then log in and use the app.

## Templates

There are two template folders in the project. One in the KeyTracker app and one in the main project folder. The templates in the KeyTracker app are for the app itself. The templates in the main project folder are there to override the default login, signup, passzord reset and other auth pages.

## Future plans

### Add login using GitHub

Login is now handled internally, but I would like to make the use of the app as easy as possible. Having users not have to create an account would be a good start. I would like to add the ability to login using GitHub. This would require the user to have a GitHub account, but normally speaking, ITF students already have one.
