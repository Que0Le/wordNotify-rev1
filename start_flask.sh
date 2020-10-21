export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
FLASK_DEBUG=0 flask run --no-reload --host=0.0.0.0