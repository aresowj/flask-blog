# -*- coding: utf-8; -*-

from flask import render_template, url_for, request, flash, session, redirect
from models import Post, User, Authentication
from utilities import admin_required, login_required, Pagination
from forms import PostEditForm, RegisterForm, LoginForm
from app import app


@app.route('/', defaults={'page': 1, 'tag_name': None})
@app.route('/page-<int:page>')
@app.route('/tag/<tag_name>', defaults={'page': 1})
@app.route('/tag/<tag_name>/page-<int:page>')
def index(page=1, tag_name=None):
    posts, total_count = Post.get_posts(app.config['POSTS_PER_PAGE'],
                                        (page - 1) * app.config['POSTS_PER_PAGE'], tag_name=tag_name)
    pagination = Pagination(page, app.config['POSTS_PER_PAGE'], total_count)

    return render_template('index.html', posts=posts, pagination=pagination, tag_name=tag_name)


@app.route('/posts', defaults={'page': 1})
@app.route('/posts/page-<int:page>')
@admin_required()
def posts_list(page=None):
    posts, total_count = Post.get_posts(app.config['POSTS_PER_PAGE'], (page - 1) * app.config['POSTS_PER_PAGE'])
    pagination = Pagination(page, app.config['POSTS_PER_PAGE'], total_count)

    return render_template('posts.html', posts=posts, pagination=pagination)


@app.route('/categories')
@admin_required()
def categories_list():
    for cat in app.config['categories']:
        print(cat.children)
    return render_template('categories_manage.html')


@app.route('/posts/<int:post_id>', methods=['GET'])
@app.route('/posts/<int:post_id>/<string:post_name>', methods=['GET'])
def post_view(post_id=None, post_name=None):
    post = Post.get_post_by_id(post_id)
    # update post view count when it is shown, calculate the view count in a simple way
    Post.increase_post_view_by_one(post)

    return render_template('post_view.html', post=post)


@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@app.route('/posts/add', methods=['GET', 'POST'])
@admin_required()
def post_edit(post_id=None):
    if post_id:
        post = Post.get_post_by_id(post_id)
        print("Post %s " % post)
        success_message = app.config['POST_EDIT_SUCCEED']
    else:
        post = Post()
        success_message = app.config['POST_ADD_SUCCEED']

    form = PostEditForm(request.form, post)

    if request.form:
        if form.validate():
            if Post.update_post(post, form):
                flash(success_message, 'success')
                return redirect(url_for('post_edit', post_id=post.id))
        else:
            flash(app.config['FORM_ERROR'], 'error')

    available_tags = list(app.config['post_tags'].keys())
    return render_template('post_edit.html', form=form, tags=available_tags)


@app.route('/post/<int:post_id>/delete/', methods=['GET'])
@admin_required()
def delete_post(post_id=None, redirect_target='index'):
    if Post.delete_post_by_id(post_id):
        flash(app.config['POST_DELETE_SUCCESS'], 'success')
    else:
        flash(app.config['POSTS_DELETE_FAILED'], 'error')
    return redirect(url_for(redirect_target))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.form:
        return Authentication.login(form)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required()
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm(request.form)

    if request.form and form.validate():
        user = User()
        form.populate_obj(user)
        if user.update_user():
            flash(app.config['REGISTRATION_SUCCEED'], 'success')
            return redirect(url_for('login'))
        else:
            flash(app.config['REGISTRATION_FAILED'], 'error')
            return redirect(url_for('sign_up'))

    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')
