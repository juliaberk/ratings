"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Rating, Movie, connect_to_db, db)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_user():
    """Register user"""

    return render_template("register.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Update database with new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    email_check = User.query
    email_check = email_check.filter(User.email == email).first()

    if email_check is not None:
        flash('This user already exists in the database')
        # Return error; user already registered
        return render_template('register.html')
    else:
        # send user information to database
        user_to_add = User(email=email, password=password)
        db.session.add(user_to_add)
        db.session.commit()
        flash('New user created!')
        session['user'] = (email, password,)

        return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
