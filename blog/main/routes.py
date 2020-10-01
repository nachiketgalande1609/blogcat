from flask import render_template, request, Blueprint, redirect, url_for, flash, abort, Blueprint
from blog.models import Post
from blog import db
from blog.main.forms import CommentForm
main = Blueprint('main', __name__)

# /////////////////////////////////// ROUTE FOR HOME ////////////////////////////////////
# ---------------------------------------------------------------------------------------
@main.route("/")
@main.route("/home")
def home():
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts, form=form)

# /////////////////////////////////// ROUTE FOR ABOUT ///////////////////////////////////
# ---------------------------------------------------------------------------------------

@main.route("/about")
def about():
    return render_template('about.html', title='About')
