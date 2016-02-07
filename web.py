# encoding = utf-8

import config
from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from forms import NewPost, RegisterForm, LoginForm
from utilities import admin_required, login_required, Pagination
from models import Base, Post, User, Category, Tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)

# initialize database connection
db = create_engine(app.config['CONNECTION_STRING'], encoding=app.config['DB_CHARSET'], echo=True)
Session = sessionmaker(bind=db)
db_session = Session()
app.db_session = db_session


# for debug purpose
def init_db():
    Base.metadata.create_all(bind=db)

try:
    db_session.query(Post).all()
    db_session.query(User).all()
    db_session.query(Category).all()
except:
    init_db()

# create tag dictionary for app-wide use
all_tags = db_session.query(Tag).all()


# get some global objects
app.config['post_tags'] = {}
for tag in all_tags:
    app.config['post_tags'][tag.name] = tag.id

app.config['categories'] = db_session.query(Category).all()


@app.route('/', defaults={'page': 1, 'tag': None})
@app.route('/page-<int:page>')
@app.route('/tag/<string:tag>', defaults={'page': 1})
@app.route('/tag/<string:tag>/page-<int:page>')
def index(page=1, tag=None):
    posts, total_count = Post.get_posts(app.config['POSTS_PER_PAGE'], (page - 1) * app.config['POSTS_PER_PAGE'], tag=tag)
    pagination = Pagination(page, app.config['POSTS_PER_PAGE'], total_count)

    return render_template('index.html', posts=posts, pagination=pagination, tag=tag)


@app.route('/posts', defaults={'page': 1})
@app.route('/posts/page-<int:page>')
@admin_required()
def posts_list(page=None):
    posts, total_count = Post.get_posts(app.config['POSTS_PER_PAGE'], (page - 1) * app.config['POSTS_PER_PAGE'])
    pagination = Pagination(page, app.config['POSTS_PER_PAGE'], total_count)

    return render_template('posts_manage.html', posts=posts, pagination=pagination)


@app.route('/categories')
@admin_required()
def categories_list():
    for cat in app.config['categories']:
        print(cat.children)
    return render_template('categories_manage.html')


@app.route('/post/<int:post_id>/<string:post_name>', methods=['GET'])
def show_post(post_id=None, post_name=None):
    post = Post.get_post_by_id(post_id)
    if post.name != post_name:
        return abort(404)

    # update post view count when it is shown
    post.view_count += 1
    app.db_session.add(post)
    app.db_session.commit()

    return render_template('post.html', post=post)


@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@app.route('/post/new/', methods=['GET', 'POST'])
@admin_required()
def edit_post(post_id=None):
    post = Post.get_post_by_id(post_id)
    form = NewPost(request.form, post)
    available_tags = list(app.config['post_tags'].keys())

    if request.form and form.validate():
        post.title = form.title.data
        post.content = form.content.data
        # only accept alphabets, numbers, underscore and slash in post name
        post.name = ''.join(char for char in form.name.data if char.isalnum() or char in ['-', '_'])
        # process tags, transfer the string into tag objects and append to the many-to-many relationship
        tags = form.tags.data.split(',')
        # clear existing tags, then re-append all tags from the form
        post.tags = []
        for tag in tags:
            # if the tag is new and not created before, insert it into tags table
            if tag not in app.config['post_tags']:
                new_tag = Tag(name=tag)
                post.tags.append(new_tag)
                app.config['post_tags'][new_tag.name] = new_tag.id
            else:
                post.tags.append(db_session.query(Tag).filter(Tag.name == tag).first())
        if not post.author_id:  # insert author id for new posts
            post.author_id = session['user_id']
        else:   # update last modify time for existing posts
            post.last_modified = datetime.now()
        app.db_session.add(post)
        app.db_session.commit()

        return redirect(url_for('edit_post', post_id=post.id, tags=available_tags))

    return render_template('post_edit.html', form=form, tags=available_tags)


@app.route('/post/delete/<int:post_id>', methods=['GET'])
@admin_required()
def delete_post(post_id=None, redirect_target='index'):
    try:
        post = Post.get_post_by_id(post_id)
        app.db_session.delete(post)
        app.db_session.commit()
        flash(app.config['POST_DELETE_SUCCESS'], 'success')
        return redirect(url_for(redirect_target))
    except:
        flash(app.config['POSTS_DELETE_FAILED'], 'error')
        return redirect(url_for(redirect_target))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.form:
        return User.login(form)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required()
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if app.db_session.query(User).count() > 0:
        flash(app.config['REGISTRATION_NOT_ALLOWED'], 'error')
        return redirect(url_for('index'))
    form = RegisterForm(request.form)

    if request.form and form.validate():
        user = User()
        form.populate_obj(user)
        try:
            user.update_user()
        except:
            flash(app.config['REGISTRATION_FAILED'], 'error')
            return redirect(url_for('sign_up'))
        else:
            flash(app.config['REGISTRATION_SUCCEED'], 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host=app.config['SERVER_ADDRESS'], port=app.config['SERVER_PORT'], debug=app.config['DEBUG'])
