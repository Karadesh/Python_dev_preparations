from flask import (render_template, url_for, flash,
    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import  db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)
@posts.route("/allpost")
@login_required
def allpost():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=5)
    return render_template('allpost.html', posts=posts)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post is created!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html', title='New post',  form=form, legend = 'New post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post is being updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend= 'Update post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post is deleted!', 'success')
    return redirect(url_for('posts.allpost'))