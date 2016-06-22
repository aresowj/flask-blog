from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, IntegerField
from wtforms.compat import text_type
from wtforms.validators import DataRequired, Email, EqualTo
from utilities import password_strength, user_exists


class TagInputField(StringField):
    def _value(self):
        if not isinstance(self.data, str):
            tag_names = []
            if self.data:
                for tag in self.data:
                    tag_names.append(tag.name)
            return text_type(','.join(tag_names)) if tag_names is not None else ''
        else:
            return super(TagInputField, self)._value()


class PostEditForm(Form):
    id = IntegerField('ID', id='id')
    title = StringField('Title', id='title', validators=[DataRequired()])
    content = TextAreaField('Content', id='content', validators=[DataRequired()])
    name = StringField('Name', id='name', validators=[DataRequired()])
    tags = TagInputField('Tags', id='tags')


class RegisterForm(Form):
    email = StringField('Email', id='email', validators=[DataRequired(), Email(), user_exists])
    name = StringField('Nickname', id='name', validators=[DataRequired()])
    password = PasswordField('Password', id='password', validators=[DataRequired(), password_strength])
    password_confirm = PasswordField('Password (Confirm)', id='password_confirm',
                                     validators=[EqualTo('password', message='Passwords must match!')])


class LoginForm(Form):
    email = StringField('Username (Your Email)', id='email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='password', validators=[DataRequired()])
    remember = BooleanField('Remember me (31 days)', id='remember')
