from flask import render_template, request, Blueprint, redirect, url_for, flash, abort, Blueprint
from blog.models import Post, Likers, User
from flask_login import current_user, login_required
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
    post_ids = [post.id for post in posts.items]  # Assuming 'items' contains the list of posts
    likers_list = User.query.join(Likers).filter(Likers.post_id.in_(post_ids)).all()

    return render_template('home.html', posts=posts, form=form, likers=likers_list)

@main.route("/like/<int:post_id>", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    likers = Likers.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if likers is None:
        likers = Likers(post_id=post.id, user_id=current_user.id)
        post.likes += 1
        db.session.add(likers)
    else:
        post.likes -= 1
        db.session.delete(likers)

    db.session.commit()

    likers_list = User.query.join(Likers).filter(Likers.post_id == post.id).all()
    
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts, form=form, post=post, likers=likers_list)

# /////////////////////////////////// ROUTE FOR ABOUT ///////////////////////////////////
# ---------------------------------------------------------------------------------------

@main.route("/about")
def about():
    return render_template('about.html', title='About')
