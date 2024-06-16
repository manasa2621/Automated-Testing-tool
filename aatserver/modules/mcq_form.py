from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
# you can use the validation error for point or difficult to ensure it is number or value or one of the choices. 

class MCQuestions(FlaskForm):
    assignment_id = IntegerField('Assignment ID')
    tag = StringField('Tag', validators=[DataRequired()])
    difficulty = SelectField('Difficulty level!', choices=[('Easy'),('Intermediate'),('Hard')], validators=[DataRequired()])
    points = IntegerField('Marks Available', validators=[DataRequired(), NumberRange(min=0)])
    question = StringField('Test Question', validators=[DataRequired()])
    opt_1 = StringField('Incorrect Answer 1', validators=[DataRequired()])
    opt_2 = StringField('Incorrect Answer 2', validators=[DataRequired()])
    opt_3 = StringField('Incorrect Answer 3', validators=[DataRequired()])
    opt_4 = StringField('Incorrect Answer 4', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])

