from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, URLField, SelectField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, URL, EqualTo
from flask_ckeditor import CKEditorField


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Task Title", validators=[DataRequired()])
    body = TextAreaField('Task Body' )
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    name = StringField("UserName", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm password", validators=[DataRequired()])
    occupation = StringField("profession", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = URLField('Cafe location on Google Maps (URL)', validators=[DataRequired()])
    cafe_price = StringField('Coffee price e.g $1.5 - 5.00', validators=[DataRequired()])
    img_url = URLField('Cafe photo (URL)', validators=[DataRequired()])
    seats = SelectField('Seats', choices=['💺', '💺💺', '💺💺💺', '💺💺💺💺', '💺💺💺💺💺'])
    can_take_calls = SelectField('Phone Calls Allowed', choices=['❌', '✅', ])
    cafe_rating = SelectField('Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi_rating = SelectField('Wifi Rating', choices=['❌', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_socket = SelectField('Power socket Rating',
                               choices=['❌', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    address = StringField('Address', validators=[DataRequired()])
    toilet = StringField('Toilet e.g Yes/No', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditCafeForm(FlaskForm):
    price = StringField("New price", validators=[DataRequired()])
    submit = SubmitField("Done")
