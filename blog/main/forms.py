from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')
