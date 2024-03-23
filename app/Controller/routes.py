from __future__ import print_function
import sys
from flask import Blueprint
from app.Controller.forms import PostForm, SortForm
from app.Model.models import Tag, postTags
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from config import Config


from app import db
from app.Model.models import Post
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])

@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sendPosts = Post.query.order_by(Post.timestamp.desc())
    sform = SortForm()
    if sform.validate_on_submit():
        sort = int(sform.sort.data)
        if sform.only_mine.data:
            if sort == 4: 
                sendPosts = current_user.get_user_posts().order_by(Post.happiness_level.desc())
            elif sort == 3:
                sendPosts = current_user.get_user_posts().order_by(Post.likes.desc())
            elif sort == 2:
                sendPosts = current_user.get_user_posts().order_by(Post.title.desc())
            elif sort == 1:
                sendPosts = current_user.get_user_posts().order_by(Post.timestamp.desc())
        else:
            if sort == 4:
                sendPosts = Post.query.order_by(Post.happiness_level.desc())
            elif sort == 3:
                sendPosts = Post.query.order_by(Post.likes.desc())
            elif sort == 2:
                sendPosts = Post.query.order_by(Post.title.desc())
            elif sort == 1:
                sendPosts = Post.query.order_by(Post.timestamp.desc())

    return render_template('index.html', title="Smile Portal", form=sform, posts=sendPosts.all())


@bp_routes.route('/postsmile', methods=['GET', 'POST'])
@login_required
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
            selectedTags = pform.tag.data
            newPost = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data, user_id = current_user.id)
            for tag in selectedTags:
                newPost.tags.append(tag)
            db.session.add(newPost)
            db.session.commit()
            flash("Your post has been created. Post title: " + pform.title.data)
            return redirect(url_for('routes.index'))
    return render_template('create.html', form=pform)

@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    getPost = Post.query.filter_by(id=post_id).first()
    getPost.likes += 1
    db.session.commit()
    return redirect(url_for('routes.index'))
