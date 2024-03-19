from __future__ import print_function
import sys
from flask import Blueprint
from app.Controller.forms import PostForm
from app.Model.models import Tag, postTags
from flask import render_template, flash, redirect, url_for, request
from config import Config


from app import db
from app.Model.models import Post
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all())


@bp_routes.route('/postsmile', methods=['GET', 'POST'])
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
            newPost = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data)
            db.session.add(newPost)
            db.session.commit()
            flash("Your post has been created. Post title: " + pform.title.data)
            return redirect(url_for('routes.index'))
    return render_template('create.html', form=pform)

@bp_routes.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    getPost = Post.query.filter_by(id=post_id).first()
    getPost.likes += 1
    db.session.commit()
    return redirect(url_for('routes.index'))
