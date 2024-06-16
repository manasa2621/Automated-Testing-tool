# Automated Testing Tool

## Overview
The Automated Testing Tool is a web application designed to facilitate the creation and administration of assessments. Staff members can upload questions as images, specify options, set correct answers, and assign marks. Students can select their level, take assessments, view their scores, and provide feedback. Staff can review the feedback provided by students.

## Features

### For Staff
- **Login:** Secure login for staff members to access the system.
- **Upload Questions:** Staff can upload questions in image format.
- **Specify Options:** Define multiple-choice options for each question.
- **Set Correct Answers:** Indicate the correct answer for each question.
- **Assign Marks:** Allocate marks for each question.
- **View Feedback:** Review feedback submitted by students after assessments.

### For Students
- **Select Level:** Choose the difficulty level or category of the assessment.
- **Take Assessment:** Answer the questions presented during the assessment.
- **View Score:** Get immediate feedback on performance with a detailed score report.
- **Provide Feedback:** Submit feedback on the assessment, which is visible to staff.

## Usage

### Staff Workflow
1. **Login:** Staff members log into the system using their credentials.
2. **Upload Question:** Navigate to the 'Upload Question' section.
   - Upload an image of the question.
   - Specify the answer options.
   - Set the correct answer.
   - Assign marks to the question.
   - Save the question to the database.
3. **View Feedback:** Access the 'Feedback' section to see feedback from students regarding assessments.

### Student Workflow
1. **Select Level:** Choose the desired level or category for the assessment.
2. **Take Assessment:** Start the assessment and answer the questions.
3. **View Score:** Submit the assessment to receive a score report.
4. **Provide Feedback:** After viewing the score, submit feedback about the assessment experience.

## Feedback System
- **Student Feedback:** After completing an assessment, students can provide feedback on the questions and overall experience.
- **Staff Review:** Staff members can view the feedback to improve future assessments and address any issues raised by students.

## Technologies Used
- **Flask:** Backend framework to handle web requests and responses.
- **SQLite:** Database to store user data, questions, options, answers, scores, and feedback.
- **HTML/CSS:** Frontend technologies for creating user interfaces.
- **JavaScript:** To add interactivity to the web pages.
- **Bootstrap:** CSS framework to design responsive and visually appealing web pages.

## Contact
For any questions or inquiries, please contact manasa.m2621@gmail.com
