# -*- coding: utf-8 -*-

"""Definitions for blog models
"""

import logging
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Sequence, DateTime, func, Table
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import current_app as app, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .web import DBSession


Base = declarative_base()


post_tags = Table('post_tag', Base.metadata,
                  Column('post_id', Integer, ForeignKey('posts.id')),
                  Column('tag_id', Integer, ForeignKey('tags.id'))
                  )
logger = logging.getLogger(__name__)


def fetch_all_instances(model):
    """Get all instances of the model from database"""
    db_session = DBSession()
    instances = db_session.query(model).all()
    db_session.close()
    return instances


def fetch_instance_by_primary_key(model, primary_key):
    if not primary_key:
        return None

    db_session = DBSession()

    try:
        return db_session.query(model).filter(model.id == primary_key)
    except NoResultFound:
        logger.error("No instance found for %s with id=%s" % (model.__class__, primary_key))
        return None
    except MultipleResultsFound:
        logger.error("Multiple instance found for %s with id=%s" % (model.__class__, primary_key))
        return None
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        db_session.close()


def delete_instance_by_primary_key(model, primary_key):
    """Delete a certain model instance by its primary key"""
    db_session = DBSession()

    try:
        instance = db_session.query(model).filter(model.id == primary_key)
        db_session.delete(instance)
        db_session.commit()
        db_session.close()
    except NoResultFound:
        logger.error("No instance found for %s with id=%s" % (model.__class__, primary_key))
        return False
    except MultipleResultsFound:
        logger.error("Multiple instance found for %s with id=%s" % (model.__class__, primary_key))
        return False
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        db_session.close()

    return True


class Authentication(object):
    @staticmethod
    def login(form):
        username = form.username.data
        password = form.password.data
        db_session = DBSession()

        try:
            user = db_session.query(User).filter(User.email == username).one()
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

        db_session.close()

        return redirect(url_for('login'))
    

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
            try:
                # no user id populated, adding new user
                self.password = generate_password_hash(self.password, method='pbkdf2:sha256')
                db_session = DBSession()
                db_session.add(self)
                db_session.commit()
                db_session.close()
                return True
            except DBAPIError as e:
                logger.exception(e)
                return False
        else:
            # has user id, updating existing user
            # update user record with id here, only touch the fields modified
            raise NotImplementedError

    @staticmethod
    def get_user_by_email(email):
        """get user by email
        :param email: the email of that user
        :return:
        """
        db_session = DBSession()
        
        try:
            user = db_session.query(User).filter(User.email == email).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None
        finally:
            db_session.close()
            
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
        db_session = DBSession()
        
        if tag_name:
            total_count = db_session.query(Post).join(Post.tags).filter(Tag.name == tag_name).count()
            posts = (db_session.query(Post).options(joinedload('tags'))
                     .filter(Post.tags.any(Tag.name == tag_name)).order_by(Post.id.desc())[skip:skip + limit])
        elif query:
            raise NotImplementedError
        else:
            total_count = db_session.query(Post.id).count()
            posts = db_session.query(Post).options(joinedload('tags')).order_by(Post.id.desc())[skip:skip + limit]

        db_session.close()
        
        return posts, total_count

    @staticmethod
    def update_post(post, form):
        db_session = DBSession()
        
        try:
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
                if form_tag and form_tag not in app.config['post_tags']:
                    new_tag = Tag(name=form_tag)
                    post.tags.append(new_tag)
                    app.config['post_tags'][new_tag.name] = new_tag.id
                else:
                    post.tags.append(db_session.query(Tag).filter(Tag.name == form_tag).first())
            if not post.author_id:  # insert author id for new posts
                post.author_id = session['user_id']
            else:  # update last modify time for existing posts
                post.last_modified = datetime.now()
            
            db_session.add(post)
            db_session.commit()
            
            return True
        except DBAPIError as e:
            logger.exception(e)
            return False
        finally:
            db_session.close()

    @staticmethod
    def delete_post_by_id(post_id):
        db_session = DBSession()
        db_session.delete(Post(post_id))
        db_session.commit()
        db_session.close()

    @staticmethod
    def get_post_by_id(post_id=None):
        return fetch_instance_by_primary_key(Post, post_id)

    @staticmethod
    def increase_post_view_by_one(post):
        if post:
            post.view_count += 1
            db_session = DBSession()
            db_session.add(post)
            db_session.commit()
            db_session.close()


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
    
    @staticmethod
    def get_all_tags():
        return fetch_all_instances(Tag)
