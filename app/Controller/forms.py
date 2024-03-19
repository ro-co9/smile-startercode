from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post, Tag

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post Message', validators=[DataRequired(), Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    def query_factory():
        return Tag.query
    def get_label(tag):
        return tag.name

    tag = QuerySelectMultipleField( 'Tag', query_factory=query_factory, get_label=get_label, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sort = SelectField('Sort By',choices = [(4, 'Happiness Level'),(3, 'Number of Likes'), (2, 'Title'), (1,'Date')])
    submit = SubmitField('Refresh')
