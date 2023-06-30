from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

session_responses = "responses"


@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('index.html', survey=survey)


@app.route('/start', methods=['POST'])
def set_responses():
    """Sets session['responses'] to an empty list"""
    session[session_responses] = []
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def handle_question():
    """Saves answer and redirects to next question, or completes the survey"""
    choice = request.form['answer']

    responses = session.get('responses', [])
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:question_num>')
def show_question(question_num):
    """Current Question"""

    responses = session.get(session_responses)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    if (len(responses) != question_num):
        flash('Invalid question access. Please answer the questions in order.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[question_num]
    return render_template("question.html", question=question)


@app.route("/complete")
def complete():
    """Show completion page."""

    return render_template("complete.html")
