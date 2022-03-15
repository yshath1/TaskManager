from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
import random
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from flask_gravatar import Gravatar
from form import CafeForm, CreatePostForm, RegisterForm
from datetime import date

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = "SECRET_KEY"
# app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)
##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///task.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    posts = relationship("TaskPost", back_populates="author")


class TaskPost(db.Model):
    __tablename__ = "task_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)


@app.route("/")
def create_new():
    return render_template("index.html", post=CreatePostForm())


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    create_post = CreatePostForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('register'))
        # hashing and salting password
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            username=form.username.data,
            password=hash_and_salted_password,
            profession=form.occupation.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        user = User.query.filter_by(email=form.email.data).first()
        return render_template("index.html", user=user, post=create_post)

    return render_template("register.html", form=form, current_user=current_user)


@app.route("/show_post", methods=["GET", "POST"])
@login_required
def show_post():
    create_post = CreatePostForm()
    if current_user.is_authenticated:
        if create_post.validate_on_submit():
            add_task = TaskPost(
                title=create_post.title.data,
                body=create_post.body.data,
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(add_task)
            db.session.commit()
            create_post.title.data = ""
            create_post.body.data = ""
            requested_post = TaskPost.query.filter_by(author_id=current_user.id).all()

            return render_template("index.html", user=current_user, post=create_post, requested_post=requested_post)
    return render_template("index.html", user=current_user, post=create_post)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    digit_post_id=int(post_id)
    create_post = CreatePostForm()
    if current_user.is_authenticated:
        requested_post = TaskPost.query.filter_by(author_id=current_user.id).all()
        for x in requested_post:
            if x.id == digit_post_id:
                db.session.delete(x)
                db.session.commit()
                return redirect(url_for('show_post'))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
