set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=0
flask init-db
flask run --no-reload --host=0.0.0.0