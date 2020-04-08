import os, base64

from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flaskr import handyfunctions

# global_config = None
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    # Load config from config.json
    from flaskr import localClass
    sf = localClass.SettingFile()
    # global_config = sf.readConfigFile()
    # print(global_config)

    app = Flask(__name__, instance_relative_config=True)

    global_config = sf.readConfigFile()
    error = sf.verify_config(global_config)
    if error != "":
        # TODO: improve return code
        return None

    # user = global_config["settings"]["API_username"]
    # password = global_config["settings"]["API_password"]
    # users = {
    #     user: generate_password_hash(password),
    #     "jerry": generate_password_hash("ThatisJerry")
    # }
    # encoded_u = base64.b64encode((user+":"+password).encode()).decode()

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, "testdb.db"),
        DATABASE="testdb.db",
        GLOBAL_CONFIG=global_config,
        GLOBAL_SF=sf,
        THREAD_STARTED=0,
        # USERS=users,
        # ENCODED_U=encoded_u,
    )
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    cors = CORS(app, resources={r"/": {"origins": "*"}})

    handyfunctions.update_config(global_config, app)
    # print(app.config)
    if app.config['THREAD_STARTED'] == 0:
        thread = localClass.NotifierThead(app)
        thread.start()
        print("started thread!")
        app.config['THREAD_STARTED'] = 1

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog, api

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(api.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
