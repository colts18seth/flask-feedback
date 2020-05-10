from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import Register_Form, Login_Form, Feedback_Form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_route():
    """ root redirect to register """
    return redirect("/register")



@app.route("/register", methods=['GET', 'POST'])
def register_route():
    """ Handle new user form """
    form = Register_Form()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()

        if user:
            session["user_id"] = user.username
            return render_template("user_details.html", user=user)
        else:
            form.username.errors = ["Bad username/password"]

    else:
        return render_template("register.html", form=form)



@app.route("/login", methods=['GET', 'POST'])
def login_route():
    """ Handle new login form """
    form = Login_Form()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        
        if user:
            session["user_id"] = user.username
            return render_template("user_details.html", user=user)
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)



@app.route("/logout")
def logout_route():
    """ Logout user """
    session.pop("user_id")

    return redirect("/")


################################################################################
# users routes
################################################################################

@app.route("/users/<username>")
def user_details_route(username):
    """ user details page """

    if "user_id" not in session or session["user_id"] != username:
        return redirect("login")
    else:
        return render_template("user_details.html", user=user)



@app.route("/users/<username>/delete", methods=['POST'])
def delete_user_route(username):
    """ Delete user """
    try:
        user = User.query.get_or_404(username)
    except:
        return redirect("/login")

    session.pop("user_id")
    db.session.delete(user)
    db.session.commit()

    return redirect("/login")