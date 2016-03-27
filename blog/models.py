from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Sequence, DateTime, func, Table
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import current_app as app, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


post_tags = Table('post_tag', Base.metadata,
                  Column('post_id', Integer, ForeignKey('posts.id')),
                  Column('tag_id', Integer, ForeignKey('tags.id'))
                  )


class User(Base):
    """Define user model"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    name = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    def get_user(self, user_id=None):
        raise NotImplementedError

    def update_user(self):
        if not self.id:
            # no user id populated, adding new user
            self.password = generate_password_hash(self.password, method='pbkdf2:sha256')
            app.db.add(self)
            app.db.commit()
            return True
        else:
            # has user id, updating existing user
            # update user record with id here, only touch the fields modified
            raise NotImplementedError

    @staticmethod
    def login(form):
        username = form.username.data
        password = form.password.data

        try:
            user = app.db.query(User).filter(User.email == username).one()
        except NoResultFound:
            flash(app.config['LOGIN_FAILED_USER_NOT_EXIST'], 'error')
        except MultipleResultsFound:
            flash(app.config['LOGIN_FAILED_DUPLICATED_USER'], 'error')
        else:
            if not check_password_hash(user.password, password):
                flash(app.config['LOGIN_FAILED_PASSWORD_NOT_MATCH'], 'error')
            else:
                # if password matched
                session['permanent'] = form.remember.data
                session['username'] = form.username.data
                session['is_admin'] = user.is_admin
                session['user_id'] = user.id
                return redirect(url_for('index'))

        return redirect(url_for('login'))

    @staticmethod
    def get_user_by_email(email):
        """
        get user by email
        :param email: the email of that user
        :return:
        """
        
        try:
            user = app.db.query(User).filter(User.email == email).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None
        return user


class Post(Base):
    """Define post model"""
    __tablename__ = 'posts'

    id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    created_time = Column(DateTime, nullable=False, default=datetime.now())
    last_modified = Column(DateTime, nullable=False, default=created_time)
    view_count = Column(Integer, nullable=True, default=0)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', backref=backref('posts', order_by=id))
    tags = relationship('Tag', secondary=post_tags, backref='posts')

    @staticmethod
    def get_posts(limit, skip, tag_name=None, query=None):
        posts = []
        total_count = 0
        if tag_name:
            total_count = app.db.query(Post).join(Post.tags).filter(Tag.name == tag_name).count()
            posts = (app.db.query(Post).options(joinedload('tags'))
                     .filter(Post.tags.any(Tag.name == tag_name)).order_by(Post.id.desc())[skip:skip + limit])
        elif query:
            pass
        else:
            total_count = app.db.query(Post.id).count()
            posts = app.db.query(Post).options(joinedload('tags')).order_by(Post.id.desc())[skip:skip + limit]
        return posts, total_count

    @staticmethod
    def get_post_by_id(post_id=None):
        if not post_id:
            return Post()
        post = app.db.query(Post).get(post_id)

        return post


class Attachment(Base):
    """Define attachment model"""

    __tablename__ = 'attachments'

    id = Column(Integer, Sequence('attachment_id_seq'), primary_key=True)
    file_type = Column(String(20), default='image')
    file_url = Column(Text)
    uploader_id = Column(Integer, ForeignKey('users.id'))

    uploader = relationship('User', backref=backref('attachments', order_by=id))


class Category(Base):
    """
    Define category model
    Categories with a None parent_id will be the top level
    """

    __tablename__ = 'categories'

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    verbose_name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), default=None)

    children = relationship('Category')


class Tag(Base):
    """
    Define tag model
    """

    __tablename__ = 'tags'

    id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name
