"""Blogly application."""

from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import FileStorage

from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def home():
    return redirect("/users")


@app.route("/users")
def users_home():
    users = User.query.all()
    return render_template("users-home.html", users=users)


@app.route("/users/new")
def render_user_form():
    return render_template("add-user-form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    # TO DO: get user data from form using request.form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    user_image = request.form["user_image"]
    new_user = User(first_name=first_name,
                    last_name=last_name, user_image=user_image)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/")
def user_details_page(user_id):
    found_user = User.query.get_or_404(user_id)
    return render_template("user-details-page.html", user=found_user)


@app.route("/users/<int:user_id>/edit")
def render_user_edit_form(user_id):
    found_user = User.query.get_or_404(user_id)
    return render_template("user-edit-form.html", user=found_user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_info(user_id):
    found_user = User.query.get_or_404(user_id)
    found_user.first_name = request.form["first_name"]
    found_user.last_name = request.form["last_name"]
    found_user.user_image = request.form["user_image"]
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect(f"/users")
