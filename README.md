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

### Running the tests
Simply run

    pytest

To automatically run all test_*.py files. 

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

### Notes

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like
development mode (which also enables features like hot reloading when you make a file change).

When running `setup.sh`, the `.env.template` file will be copied to `.env` if the latter does not exist.

### Required .env Vars
As it stands, there are some variables that are required for the app to work (see `.env.template`) for example.
    
    # Represents the API key an token that you will need to retrieve from trello
    TRELLO_KEY=XXXX
    TRELLO_TKN=YYYY
    # The id of the trello board that you wish the app to interact with.
    # This can be obtained by manually calling the API with postman, or via the trello site
    TRELLO_BOARD=ZZZZ