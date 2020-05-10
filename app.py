from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import Register_Form, Login_Form, Feedback_Form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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
            return redirect(f"/users/{user.username}")
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
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)



@app.route("/logout")
def logout_route():
    """ Logout user """
    session.pop("user_id")

    return redirect("/login")


########################################################################
# users routes
########################################################################

@app.route("/users/<username>")
def user_details_route(username):
    """ user details page """

    user = User.query.filter_by(username=username).first()
    all_feedback = Feedback.query.all()

    if "user_id" not in session or session["user_id"] != username:
        return redirect("login")
    else:
        return render_template("user_details.html", user=user, feedback=all_feedback)



@app.route("/users/<username>/delete", methods=['POST'])
def delete_user_route(username):
    """ Delete user """

    if "user_id" not in session or session["user_id"] != username:
        return redirect("/register")
    else:
        user = User.query.filter_by(username=username).first()
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        return redirect("/login")



@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback_route(username):
    """ Add feedback for user with FeedbackForm """

    if "user_id" not in session or session["user_id"] != username:
        return redirect("/register")

    form = Feedback_Form()
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = user.username

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")

    return render_template("feedback_form.html", form=form, user=user)



@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback_route(feedback_id):
    """ Render feedback edit form and handle edit """

    user = User.query.filter_by(username=session["user_id"]).first()

    if "user_id" not in session or session["user_id"] != user.username:
        return redirect("/register")

    feedback = Feedback.query.filter_by(id=feedback_id).first()   
    form = Feedback_Form(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")
    
    return render_template("feedback_edit_form.html", form=form, user=user, feedback=feedback)



@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback_route(feedback_id):
    """ delete feedback from user and redirect to user details """

    user = User.query.filter_by(username=session["user_id"]).first()

    if "user_id" not in session or session["user_id"] != user.username:
        return redirect("/register")

    feedback = Feedback.query.filter_by(id=feedback_id).first()

    if request.method == "POST":        
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")
    
    else:
        return redirect("/register")