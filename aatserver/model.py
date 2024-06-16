from aatserver import db

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    is_open = db.Column(db.Integer, nullable=False)
    module = db.relationship('Module', backref='assignments')

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='attempts')
    assignment = db.relationship('Assignment', backref='attempts')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    is_staff = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class TF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    tag = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    point = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    corr_answer = db.Column(db.Integer, nullable=False)
    assignment = db.relationship('Assignment', backref='tf_questions')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'), nullable=False)
    question_type = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Text)
    user_answer_1 = db.Column(db.Text)
    user_answer_2 = db.Column(db.Text)
    user_answer_3 = db.Column(db.Text)
    user_answer_4 = db.Column(db.Text)
    user_answer_5 = db.Column(db.Text)
    user_answer_6 = db.Column(db.Text)
    attempt = db.relationship('Attempt', backref='answers')

class FormativeAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.relationship('Assignment', backref='formative_assessments')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('TF.id'))
    content = db.Column(db.Text, nullable=False)
    attempt = db.relationship('Attempt', backref='comments')
    question = db.relationship('TF', backref='comments')
