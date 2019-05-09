# impossibilicus-api
This is the simplest possible API to interact with the UI in [impossibilicus-web](https://github.com/mef79/impossibilicus-web)

## Documentation of Libraries Used
- [Flask](http://flask.pocoo.org/) - minimal python web framework
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/0.3.5/) - library that adds helpful REST conventions to Flask

## Requirements
- Python 2.7
- Python's `pip` library
  - It might be installed with Python already - try just running the command `pip` to test
  - If that fails, [Pip Installation Guide](https://pip.pypa.io/en/stable/installing/)
- `virtualenv` ([Flask's documentation on `virtualenv`](http://flask.pocoo.org/docs/0.12/installation/) is my favorite)
- MongoDB ([Documentation](https://docs.mongodb.com/manual/installation/)), confirm installation by running `mongod`

## Starting the API
- Start Mongo with `mongod` (if you're running Mongo locally, otherwise it just needs environment varibles set to reference the hosted DB)
- From the project directory, create/activate a virtual environment (step-by-step instructions also in [Flask's `virtualenv` docs](http://flask.pocoo.org/docs/0.12/installation/))
- Install the project dependencies with `pip install -r requirements.txt`
- Environment variables that need to be set for the app to work: `MONGODB_URI`, `MONGO_USERNAME` (these live permanently in Heroku, I'm not committing them because even though this is private now, something something commit history)
  - Optionally, `FLASK_DEBUG=1` to enable flask's debug mode, which will live update the app when changes are made and display more detailed error outputs
- Start the API with `python app.py`
- Confirm that it is running by accessing [`http://localhost:5000/`](http://localhost:5000/)
- Use any REST client to make API calls (I use [Insomnia](https://insomnia.rest/))

## Deploying
- Application is automatically deployed on Heroku when a new commit is pushed to master. The web app that interacts with this API can be found here: https://immense-oasis-52264.herokuapp.com/

## MongoDB Commands
- Connect (requires Mongo installed): `mongo ds147510.mlab.com:47510/database_name -u username -p password`
- Empty out a collection ("story"): `db.story.remove({})`
