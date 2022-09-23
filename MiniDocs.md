# Kiwi

## About

Kiwi, like the bird not the fruit, is a webapp that keeps track of who has one common shared key. Users can use the app to indicate they have the key or returned it to a reception desk or lockbox.

## To run the development server do

~~~
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
