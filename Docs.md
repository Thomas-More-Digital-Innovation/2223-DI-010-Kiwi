# Kiwi

## About

Kiwi, the bird not the fruit, is a webapp that keeps track of who has one common shared key. Users can use the app to indicate they have the key or returned it to a reception desk or lockbox.

## Make Tailwind update the css on changes

<https://tailwindcss.com/blog/standalone-cli>

## Windows

 ~~~ps1
./tailwindcss.exe -i keyTracker/static/keyTracker/css/input.css -o keyTracker/static/keyTracker/css/output.css --watch
 ~~~

## Linux

 ~~~shell
./tailwindcss-linux -i keyTracker/static/keyTracker/css/input.css -o keyTracker/static/keyTracker/css/output.css --watch
 ~~~

## How it works

### Sign up

When a user signs up, they enter a username, email, rnumber and password. They then need to be verified by the admin. The admin can do this by going to the django admin page and adding the newly created user to the group "DI". The user can then log in and use the app.

### Templates

There are two template folders in the project. One in the KeyTracker app and one in the main project folder. The templates in the KeyTracker app are for the app itself. The templates in the main project folder are there to override the default login, signup, passzord reset and other auth pages.

## Future plans

### Add login using school account

Github authentication was chosen because all students normally have a github account. Using their Thomas More / school account might have been even easier but required the use of Active Directory. Creating another Active Directory within the Thomas More organization was not possible.

Python Social Auth is used for github authentication. More info about it can be found here: <https://python-social-auth.readthedocs.io/en/latest/backends/github.html>

### Push notifications

Users may want to get a push notification when the key has been returnedor taken. This can be done using the django-push-notifications package.

## Deployment

TODO: collectstatic

### Django development server

You can use the development server that comes with Django itself by running

~~~python
python3 manage.py runserver
~~~

### Docker

#### Local

build the container

~~~yaml
docker compose -f docker-compose-dev.yml build
~~~

then to run it go do

~~~yaml
docker compose -f docker-compose-dev.yml up -d
~~~

to open terminal in that container:

~~~bash
docker compose -f docker-compose-dev.yml exec web bash
~~~

or

~~~bash
docker exec -it <containerId> sh
~~~

Make sure the order of the parameters is correct and the correct file is passed in both commands.
The app can now be found at <http://localhost:8000/>>

#### Production

To release a new version of the app to production, push your code and merge your branch with the master branch.
To get these changes into production, just release new tags.

~~~bash
git tag v1.0.0
git push --tags 
~~~

When this is done, Github Actions will (if the tests succeeded) run the 'build-container.yaml' file  to build the container and add it to the Github Container Registry. The container will then be pulled by the server with Watchtower and the container will be restarted. The newest changes should then be deployed.

<!-- You can also test the production deployment

~~~bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
~~~ -->
