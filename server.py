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

        return redirect("/")


@app.route('/login', methods=["GET"])
def user_login():
    """Show form to allow user to login"""

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def credential_verification():
    """Verify user credentials"""

    email = request.form.get("email")
    password_input = request.form.get("password")

    current_login = User.query # stepone
    
    current_login = current_login.filter(User.email == email).first()
    # user object

    if current_login is None: # check if database matches user input
        flash("Email is not registered, please register.")
        return redirect('/register')

    # password_input is password inputted by user
    # next step: compare password_input to password attribute on instance of user object

    elif current_login is not None:
        
        if password_input == current_login.password:

            session["current_user_id"] = current_login.user_id
            print "***TEST*** ", session['current_user_id'] 
            flash("Welcome Home! Login successful")
            return redirect("/")

        else:
            flash("SORRY NOT SORRY. Access denied.")
            return redirect("/login")


@app.route('/logout', methods=["POST"])
def user_logout():
    """Log user out of session"""

    session["current_user_id"] = None
    print "***VALUE REMOVED???*** ", session["current_user_id"]
    # should the logout button only show up is user is logged in??

    flash("User successfully logged out!")
    return redirect('/')

            
    # get email and password from form
    # check database for email and if email is in the database, check if
    # the password submitted matches password already in database. Grab ID.
    # if login doesn't work,  flash message "Your email or password does not match"
    # if login does work, add id to the session, redirected to homepage
    # flash "Login successful" message


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
