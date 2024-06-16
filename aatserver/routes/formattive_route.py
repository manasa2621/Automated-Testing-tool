from flask import render_template, url_for, jsonify, request, redirect,session, flash
from aatserver import app, db
from sqlalchemy import text
from werkzeug.utils import secure_filename
import base64
import os
import json

@app.route("/check_db_connection")
def check_db_connection():
    try:
        query = text('SELECT * FROM comment')
        cursor = db.session.execute(query)
        assessments = cursor.fetchall()
        return jsonify({"status": "success", "message": "Database connection successful"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    
    # Example authentication logic (replace with your actual authentication logic)
    if username == 'staff' and password == 'staff':
        # Redirect to staffs-view upon successful authentication
        return redirect(url_for('staffView'))
    else:
        # Add error handling for invalid credentials (optional)
        error = 'Invalid username or password. Please try again.'
        return render_template('staff-login.html', error=error)

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker



@app.route('/fetch_assessments', methods=['GET'])
def fetch_assessments():
    try:
        difficulty_level = request.args.get('difficulty_level')
        
        if difficulty_level:
            query = text('SELECT * FROM assessment WHERE difficulty_level = :difficulty_level')
            assessments = db.session.execute(query, {'difficulty_level': difficulty_level}).fetchall()
        else:
            query = text('SELECT * FROM assessment')
            assessments = db.session.execute(query).fetchall()
        
        assessments_data = []
        for assessment in assessments:
            assessments_data.append({
                'id': assessment.id,
                'name': assessment.name,
                'difficulty_level': assessment.difficulty_level,
                'total_questions': assessment.total_questions,
                'total_marks': assessment.total_marks
            })
        
        return jsonify({"status": "success", "assessments": assessments_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
                
@app.route('/formative_assessment')
def render_formative_assessment():
    return render_template('formative_assessment.html')

@app.route('/view_assessment/<int:assessment_id>')
def view_assessment(assessment_id):
    try:
        return render_template('view_assessment_staff.html', assessment_id=assessment_id)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return redirect(url_for('render_formative_assessment'))

from sqlalchemy import text
import base64

@app.route('/fetch_assessment_data/<int:assessment_id>')
def fetch_assessment_data(assessment_id):
    try:
        query = """
            SELECT 
                a.id AS assessment_id,
                a.name AS assessment_name,
                a.difficulty_level,
                a.total_questions,
                a.total_marks,
                q.id AS question_id,
                q.question_text,
                q.marks AS question_marks,
                q.question_type,
                c.id AS comment_id,
                c.content AS comment_content,
                o.id AS option_id,
                o.option_text,
                o.is_correct
            FROM 
                assessment a
            JOIN 
                question q ON a.id = q.assessment_id
            LEFT JOIN 
                comment c ON q.id = c.question_id
            LEFT JOIN 
                option o ON q.id = o.question_id
            WHERE 
                a.id = :id
            """
        result = db.session.execute(text(query), {"id": assessment_id}).fetchall()

        assessment_data = {}
        for row in result:
            assessment_id = row[0]
            if assessment_id not in assessment_data:
                assessment_data[assessment_id] = {
                    "assessment_id": row[0],
                    "assessment_name": row[1],
                    "difficulty_level": row[2],
                    "total_questions": row[3],
                    "total_marks": row[4],
                    "questions": {}
                }
            question_id = row[5]
            if question_id not in assessment_data[assessment_id]['questions']:
                # Convert BLOB data to base64 for safe transport to frontend
                question_text = base64.b64encode(row[6]).decode('utf-8')
                assessment_data[assessment_id]['questions'][question_id] = {
                    "question_id": row[5],
                    "question_text": question_text,
                    "question_marks": row[7],
                    "question_type": row[8],
                    "comments": [],
                    "options": []
                }
            if row[9]:
                assessment_data[assessment_id]['questions'][question_id]['comments'].append({
                    "comment_id": row[9],
                    "comment_content": row[10]
                })
            if row[11]:
                assessment_data[assessment_id]['questions'][question_id]['options'].append({
                    "option_id": row[11],
                    "option_text": row[12],
                    "is_correct": row[13]
                })

        return jsonify({"status": "success", "assessment_data": assessment_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/add_assessment')
def render_add_assessments():
    return render_template('add_assessments.html')

@app.route('/view-results')
def view_results():
    marks = request.args.get('marks')
    assessment_id=request.args.get('assessment_id')
    return render_template('view-results.html', marks=marks,assessment_id=assessment_id)

import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    try:
        # Log request form and files
        app.logger.info('Request form data: %s', request.form.to_dict())
        app.logger.info('Request files: %s', request.files)

        # Retrieve form data
        assessment_data = request.form.to_dict()
        question_files = request.files

        # Check required fields
        required_fields = ['name', 'difficulty', 'total_questions', 'total_marks']
        for field in required_fields:
            if field not in assessment_data:
                raise KeyError(f'Missing required field: {field}')

        total_questions = int(assessment_data['total_questions'])

        # Insert assessment details into the database
        db.session.execute(text("""
            INSERT INTO assessment (name, difficulty_level, total_questions, total_marks)
            VALUES (:name, :difficulty, :total_questions, :total_marks)
        """), {
            'name': assessment_data['name'],
            'difficulty': assessment_data['difficulty'],
            'total_questions': total_questions,
            'total_marks': assessment_data['total_marks']
        })
        db.session.commit()

        result = db.session.execute(text("SELECT last_insert_rowid()"))
        assessment_id = result.fetchone()[0]
        app.logger.info(f'Inserted assessment with ID: {assessment_id}')

        # Process each question file
        for i in range(total_questions):
            file_key = f'question_image-{i}'
            if file_key in question_files and allowed_file(question_files[file_key].filename):
                file = question_files[file_key]
                file_content = file.read()
                app.logger.info(f'Read file content for: {file_key}')

                # Insert question details into the database
                db.session.execute(text("""
                    INSERT INTO question (assessment_id, question_text, marks, question_type)
                    VALUES (:assessment_id, :question_text, :marks, :question_type)
                """), {
                    'assessment_id': assessment_id,
                    'question_text': file_content,  # Store the file content as BLOB
                    'marks': assessment_data[f'marks[{i}]'],
                    'question_type': assessment_data[f'question_types[{i}]']
                })
                db.session.commit()

                result = db.session.execute(text("SELECT last_insert_rowid()"))
                question_id = result.fetchone()[0]

                # Insert options details into the database
                for option_index, option_text in enumerate(request.form.getlist(f'options-{i}[]')):
                    is_correct = (option_index == int(assessment_data[f'correct_answers[{i}]']))
                    db.session.execute(text("""
                        INSERT INTO option (question_id, option_text, is_correct)
                        VALUES (:question_id, :option_text, :is_correct)
                    """), {
                        'question_id': question_id,
                        'option_text': option_text,
                        'is_correct': is_correct
                    })
                db.session.commit()

        return jsonify({"message": "Assessment submitted successfully"}), 200

    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/delete-assessment/<int:assessment_id>', methods=['DELETE'])
def delete_assessment(assessment_id):
    try:
        db.session.execute(
            text("DELETE FROM comment WHERE question_id IN (SELECT id FROM question WHERE assessment_id = :id)"),
            {"id": assessment_id}
        )

        db.session.execute(
            text("DELETE FROM option WHERE question_id IN (SELECT id FROM question WHERE assessment_id = :id)"),
            {"id": assessment_id}
        )

        db.session.execute(
            text("DELETE FROM question WHERE assessment_id = :id"),
            {"id": assessment_id}
        )

        db.session.execute(
            text("DELETE FROM assessment WHERE id = :id"),
            {"id": assessment_id}
        )

        db.session.commit()

        return jsonify({"status": "success", "message": f"Assessment {assessment_id} and associated data deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/take_assessment/<int:assessment_id>')
def take_assessment(assessment_id):
    try:
        return render_template('take-assessment.html', assessment_id=assessment_id)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return redirect(url_for('view_assessments'))

@app.route('/view_assessments')
def view_assessments():
    return render_template('view-assessments.html')

@app.route('/edit_assessment/<int:assessment_id>')
def edit_assessment(assessment_id):
    try:
        return render_template('update-assessments.html', assessment_id=assessment_id)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return redirect(url_for('formative_assessment'))

@app.route('/update-assessment/<int:assessment_id>', methods=['PUT'])
def update_assessment(assessment_id):
    try:
        updated_data = request.json

        db.session.execute(
            text("""
            UPDATE assessment 
            SET 
                name = :name, 
                difficulty_level = :difficulty,
                total_questions = :total_questions,
                total_marks = :total_marks 
            WHERE id = :id
            """),
            {
                'name': updated_data['edit_assessment_name'],
                'difficulty': updated_data['edit_difficulty_level'],
                'total_questions': updated_data['edit_total_questions'],
                'total_marks': updated_data['edit_total_marks'],
                'id': assessment_id
            }
        )

        for question_data in updated_data['questions']:
            db.session.execute(
                text("""
                UPDATE question 
                SET question_text = :question_text, 
                    marks = :marks,
                    question_type = :question_type 
                WHERE id = :id
                """),
                {
                    'question_text': question_data['question_text'],
                    'marks': question_data['question_marks'],
                    'question_type': question_data['question_type'],
                    'id': question_data['question_id']
                }
            )

            for comment_data in question_data['comments']:
                db.session.execute(
                    text("""
                    UPDATE comment 
                    SET content = :content 
                    WHERE id = :id
                    """),
                    {
                        'content': comment_data['comment_content'],
                        'id': comment_data['comment_id']
                    }
                )

        db.session.commit()

        return jsonify({"status": "success", "message": "Assessment details updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    if request.method == 'POST':
        data = request.json

        feedback = data.get('feedback')
        student_name = data.get('student_name')
        assessment_id = data.get('assessment_id')

        if feedback and student_name and assessment_id:
            try:
                db.session.execute(text("""
                    INSERT INTO feedback (feedback, student_name, assessment_id)
                    VALUES (:feedback, :student_name, :assessment_id)
                """), {
                    'feedback': feedback,
                    'student_name': student_name,
                    'assessment_id': assessment_id
                })
                db.session.commit()
                return jsonify({'message': 'Feedback submitted successfully'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing data in the request'}), 400

@app.route('/view-feedback', methods=['GET'])
def get_feedback():
    try:
        feedback_data = db.session.execute(text("""
            SELECT f.feedback, f.student_name, a.name
            FROM feedback f
            INNER JOIN assessment a ON f.assessment_id = a.id
        """)).fetchall()

        feedback_list = [{'feedback': feedback, 'student_name': student_name, 'assessment_name': assessment_name} 
                         for feedback, student_name, assessment_name in feedback_data]

        return jsonify({'feedback_list': feedback_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/viewstudent-feedback')
def view_feedback():
    return render_template('view-feedback.html')

@app.route('/view_staff_comments/<int:assessment_id>')
def view_staff_comments(assessment_id):
    try:
        return render_template('view_staff_comments.html', assessment_id=assessment_id)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return redirect(url_for('view_assessments'))

@app.route('/view_student_comments/<int:assessment_id>')
def view_student_comment(assessment_id):
    try:
        return render_template('view_student_comments.html', assessment_id=assessment_id)
    except Exception as e:
        flash("An error occurred: " + str(e))
        return redirect(url_for('view_assessments'))

@app.route('/view_student_comment/<int:assessment_id>', methods=['GET'])
def view_student_comments(assessment_id):
    student_name = request.args.get('student_name')

    if not student_name:
        return jsonify({'error': 'Missing student_name parameter'}), 400

    try:
        result = db.session.execute(text("""
            SELECT feedback
            FROM feedback
            WHERE assessment_id = :assessment_id AND student_name = :student_name
        """), {
            'assessment_id': assessment_id,
            'student_name': student_name
        })

        feedback_row = result.fetchone()

        if feedback_row:
            feedback = feedback_row[0]
            return jsonify({'feedback': feedback}), 200
        else:
            return jsonify({'message': 'You have not given feedback for this assessment'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_feedback/<int:assessment_id>', methods=['POST'])
def update_feedback(assessment_id):
    student_name = request.json.get('student_name')
    new_feedback = request.json.get('new_feedback')

    if not student_name or not new_feedback:
        return jsonify({'error': 'Missing student_name or new_feedback parameter'}), 400

    try:
        update_query = text("""
            UPDATE feedback
            SET feedback = :new_feedback
            WHERE assessment_id = :assessment_id AND student_name = :student_name
        """)

        result = db.session.execute(
            update_query,
            {
                'new_feedback': new_feedback,
                'assessment_id': assessment_id,
                'student_name': student_name
            }
        )

        db.session.commit()

        if result.rowcount > 0:
            return jsonify({'message': 'Feedback updated successfully'}), 200
        else:
            return jsonify({'message': 'Feedback not found for this assessment and student'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_comment', methods=['DELETE'])
def delete_comment():
    student_name = request.args.get('student_name')
    feedback = request.args.get('feedback')

    if not student_name or not feedback:
        return jsonify({'error': 'Missing student_name or feedback parameter'}), 400

    try:
        delete_query = text("""
            DELETE FROM feedback
            WHERE student_name = :student_name 
            AND feedback = :feedback
        """)
        result = db.session.execute(delete_query, {
            'student_name': student_name,
            'feedback': feedback
        })

        db.session.commit() 

        if result.rowcount > 0:
            return jsonify({'message': 'Feedback deleted successfully'}), 200
        else:
            return jsonify({'message': 'Feedback not found for deletion'}), 404

    except Exception as e:
        db.session.rollback()  
        return jsonify({'error': str(e)}), 500