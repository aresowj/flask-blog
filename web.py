# encoding = utf-8

import config
from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from forms import PostAddForm, RegisterForm, LoginForm
from utilities import admin_required, login_required, Pagination
from models import Base, Post, User, Category, Tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# initialize app
app = Flask(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object(config)

# initialize database connection
db_engine = create_engine(app.config['CONNECTION_STRING'], encoding=app.config['DB_CHARSET'], echo=True)
Session = sessionmaker(bind=db_engine)  # bind engine to session
db = Session()  # initialize SQLAlchemy session
app.db = db     # put session to app instance 


# for debug purpose
def init_db():
    Base.metadata.create_all(bind=db)

try:
    db.query(Post).all()
    db.query(User).all()
    db.query(Category).all()
except:
    init_db()

# create tag dictionary for app-wide use
all_tags = db.query(Tag).all()


# get some global objects
app.config['post_tags'] = {}
for tag in all_tags:
    app.config['post_tags'][tag.name] = tag.id

app.config['categories'] = db.query(Category).all()


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
    post.view_count += 1
    app.db.add(post)
    app.db.commit()

    return render_template('post_view.html', post=post)


@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@app.route('/posts/add', methods=['GET', 'POST'])
@admin_required()
def post_edit(post_id=None):
    if post_id:
        post = Post.get_post_by_id(post_id)
    else:
        post = Post()
    form = PostAddForm(request.form, post)
    available_tags = list(app.config['post_tags'].keys())

    if request.form and form.validate():
        post.title = form.title.data
        post.content = form.content.data
        # only accept alphabets, numbers, underscore and slash in post name
        post.name = ''.join(char for char in form.name.data if char.isalnum() or char in ['-', '_'])
        # process tags, transfer the string into tag objects and append to the many-to-many relationship
        form_tags = form.tags.data.split(',')
        # clear existing tags, then re-append all tags from the form
        post.tags = []
        for form_tag in form_tags:
            # if the tag is new and not created before, insert it into tags table
            if form_tag not in app.config['post_tags']:
                new_tag = Tag(name=form_tag)
                post.tags.append(new_tag)
                app.config['post_tags'][new_tag.name] = new_tag.id
            else:
                post.tags.append(db.query(Tag).filter(Tag.name == form_tag).first())
        if not post.author_id:  # insert author id for new posts
            post.author_id = session['user_id']
        else:   # update last modify time for existing posts
            post.last_modified = datetime.now()
        app.db.add(post)
        app.db.commit()

        return redirect(url_for('post_edit', post_id=post.id, tags=available_tags))

    flash(app.config['FORM_ERROR'], 'error')
    return render_template('post_edit.html', form=form, tags=available_tags)


@app.route('/post/delete/<int:post_id>', methods=['GET'])
@admin_required()
def delete_post(post_id=None, redirect_target='index'):
    try:
        post = Post.get_post_by_id(post_id)
        app.db.delete(post)
        app.db.commit()
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
    if app.db.query(User).count() > 0:
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
