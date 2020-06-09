import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.add_users import User
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')


# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')
logger.debug(app.config['SQLALCHEMY_DATABASE_URI'])

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists posts and predictions

    Create view into index page that uses data queried from User database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        user = db.session.query(User).order_by(User.id.desc()).limit(1).all()  #limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index1.html', users=user)
    except:
        traceback.print_exc()
        logger.warning("Not able to display user posts, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new user post input

    :return: redirect to index page
    """
    with open('models/modelie.pkl', "rb") as f:
        modelie = pickle.load(f)

    with open('models/modeljp.pkl', "rb") as f:
        modeljp = pickle.load(f)

    with open('models/modelns.pkl', "rb") as f:
        modelns = pickle.load(f)

    with open('models/modeltf.pkl', "rb") as f:
        modeltf = pickle.load(f)


    try:
        posts = str(request.form['posts'])
        # create features from raw user input
        words_per_comment = len(posts.split())
        http_per_comment = posts.count('http')
        music_per_comment = posts.count('music')
        question_per_comment = posts.count('?')
        img_per_comment = posts.count('jpg')
        excl_per_comment = posts.count('!')
        ellipsis_per_comment = posts.count('...')
    except:
        logger.warning("Input must be in string format, error message displayed")
        return ('Please check your input.')

    X = pd.DataFrame({'words_per_comment': [words_per_comment], 'http_per_comment': [http_per_comment],
                      'music_per_comment': [music_per_comment],
                      'question_per_comment': [question_per_comment], 'img_per_comment': [img_per_comment],
                      'excl_per_comment': [excl_per_comment], 'ellipsis_per_comment': [ellipsis_per_comment]})

    Class_ie = modelie.predict(X)
    if Class_ie == 0:
        Output_ie = 'I'
    else:
        Output_ie = 'E'

    Class_ns = modelns.predict(X)
    if Class_ns == 0:
        Output_ns = 'N'
    else:
        Output_ns = 'S'

    Class_jp = modeljp.predict(X)
    if Class_jp == 0:
        Output_jp = 'J'
    else:
        Output_jp = 'P'

    Class_tf = modeltf.predict(X)
    if Class_tf == 0:
        Output_tf = 'T'
    else:
        Output_tf = 'F'

    # concat final putput
    type_output = Output_ie + (Output_ns) + (Output_tf) + (Output_jp)

    try:
        user1 = User(posts=request.form['posts'], type=type_output)
        db.session.add(user1)
        db.session.commit()
        logger.info(
            "New user post and personality type prediction added, posts: %s,  type prediction: %s", request.form['posts'], type_output)
        return redirect(url_for('index'))
    except:
        traceback.print_exc()
        logger.warning("Not able to display posts and prediction, error page returned")
        return render_template('error.html')


@app.route('/about', methods=['POST','GET'])
def about():
    '''
    View that display basic information about MBTI personalities

    :return: redirect to about page
    '''

    try:
        return render_template('about.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to return to about.html")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])