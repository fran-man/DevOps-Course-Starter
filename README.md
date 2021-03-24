# DevOps Apprenticeship: Project Exercise

## Running with Poetry
This application has been migrated to work with poetry. In order to leverage this you will have to do a small amount of
configuration and setup

### Install Poetry

#### Windows (Powershell)
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

#### *nix (e.g. using BASH)
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    
Once this is done, run
    
    poetry --version
to check that poetry was installed correctly. If not, you may have to make sure that poetry is added to your path.

### Installing Dependencies with Poetry
Please run

    poetry add requests
    poetry install
    
### Running The App
You should now be able to run the app with:

    poetry run flask run
The app should run with similar output and behaviour to before:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running Inside Vagrant
This application has also been setup to run inside a VM with vagrant. You will need to have [vagrant](https://www.vagrantup.com/)
installed.

The vagrant file has been setup to do all of the heavy lifting when it comes to installing dependencies and running the
app, including:
- apt-get installing all the dependencies
- Setting up all the environment variables
- Uplifting default python version to 3.x
- Install poetry
- Install python libs required
- Starting the app and exposing the required port

Therefore, once you installed vagrant, all you should need to do is run

    vagrant up

And you should then see vagrant doing all the setup steps above and eventually, the output from the application.
Then you can navigate to localhost:8080 and you should see your application running!

## Running in Docker
This app has been setup to run inside docker containers

There are two options
- Development - will run the application with hot reloading, using flask
- Production - will run the application in a using production-appropriate HTTP server gunicorn

### Building
Development
    
    docker build --target development --tag todo-app:dev .
    
Production

    docker build --target production --tag todo-app:prod .
    
Feel free to customise the image name and tag to your liking.

You can then run the application directly, or by using the included docker-compose files which will handle things like 
bind mounts and exposing ports for you.

    # Using docker-compose for orchestration
    docker-compose -f docker-compose-dev.yml up
    
    # OR using docker run directly
    # Bind mount not required for production image
    docker run -p 5000:5000 --mount type=bind,source=<PROJECT_ROOT>,target=/app <image>:<tag>
    
Note that `<PROJECT_ROOT>` must be absolute.

You will then be able to view the application on http://localhost:5000/

### Testing (in docker)
The `Dockerfile` has a special stage for running tests.

To build:
    
     docker build --target test --tag <image>:<tag> .
To run:

    docker run --mount type=bind,source=<PATH_ON_LOCAL>,target=/app <image>:<tag>

### Notes

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like
development mode (which also enables features like hot reloading when you make a file change).

When running `setup.sh`, the `.env.template` file will be copied to `.env` if the latter does not exist.

When running the production docker image, no bind mount is required since `Dockerfile` copies all the files into the image

### Required .env Vars
As it stands, there are some variables that are required for the app to work (see `.env.template`) for example.
    
    # Represents the API key an token that you will need to retrieve from trello
    TRELLO_KEY=XXXX
    TRELLO_TKN=YYYY
    # The id of the trello board that you wish the app to interact with.
    # This can be obtained by manually calling the API with postman, or via the trello site
    TRELLO_BOARD=ZZZZ
    
## Travis
The application has been enhanced to allow the tests to be run by travis (inside a docker container). Please see `.travis.yml`.
The secrets are stored within travis to avoid committing them to source control. These are managed within the travis GUI.