from logging import error
import os
import sys
from flask import Flask, request, abort, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Pagenate the questions retrived
def paginate(req, questions_data):
  # Extract page number from the request
  page = req.args.get('page', 1, type=int)

  # Determinte the start and the end range
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions_on_page = [Question.format(question) for question in questions_data]

  return questions_on_page[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs✅
  '''
  # CORS(app)
  cors = CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow✅
  '''
  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.✅
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories_data = Category.query.all()
    all_categories = {categorie.id : categorie.type for categorie in categories_data}

    if categories_data is None:
      abort(404)

    return jsonify({
      'success': True,
      'categories': all_categories
    })

  '''
  @TODO:✅
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions',methods=['GET'])
  def Retrive_all():
    questions_data = Question.query.order_by(Question.id).all()

    questions = paginate(request, questions_data)

    # Return error if there is no questions found in the requested page
    if len(questions) == 0:
      abort(404)

    categories_data = Category.query.all()
    all_categories = {categorie.id : categorie.type for categorie in categories_data}

    return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions_data),
        'categories': all_categories,
        'current_category': None
    })

  '''
  @TODO:✅
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):

    # Try to delete the question using id, if not susessful return 404
    try:
      target_question = Question.query.get(id)
      target_question.delete()

      return jsonify({
        'success': True
      })

    except:
      abort(404)
  '''
  @TODO:✅
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions', methods=['POST'])
  def add_new_question():

    req = request.get_json()

    if req == None:
      abort(422)

    # Check if the request has all the required data
    if ('question' and 'answer' and 'difficulty' and 'category') not in req:
      print('missing data')
      abort(422)

    req_question = req.get('question')
    req_answer = req.get('answer')
    req_category = req.get('category')
    req_difficulty = req.get('difficulty')

    # Check if the data has a value
    if not (req_question and req_answer and req_difficulty and req_category):
      print('Data needs contex')
      abort(422)

    try:
      new_question = Question(question= req_question,
                              answer = req_answer,
                              category = req_category,
                              difficulty = req_difficulty)

      new_question.insert()

      return jsonify({
        'success': True
      })

    except :
      abort(422)
  '''
  @TODO: ✅
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():

    # parse the request body
    req = request.get_json()
    search_term = req.get('searchTerm')

    # query questions from the db using the search_term
    questions_data = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    questions = paginate(request, questions_data)

    # Return error if there is no questions found in the requested page
    if len(questions) == 0:
      abort(404)


    return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions_data),
        'current_category': None
    })



  '''
  @TODO: ✅
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:id>/questions', methods=["GET"])
  def get_questions_from_category(id):

    # query questions from the db using the category id
    questions_data = Question.query.filter(Question.category == id).all()

    questions = paginate(request, questions_data)

    # Return error if there is no questions found in the requested page
    if len(questions) == 0:
      abort(404)


    return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions_data),
        'current_category': id
    })


  '''
  @TODO:✅
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route('/quizzes', methods=['POST'])
  def quiz_question():

    # parse the request body
    req = request.get_json()


    if not ('quiz_category' and 'previous_questions') in req:
      abort(422)

    quiz_category = req.get('quiz_category')
    previous_questions = req.get('previous_questions')

    try:
      # Retrive questions that are not in previous_questions
      # If category is provided query using it else retrive all question
      if quiz_category['id'] == 0:
        questions_data = Question.query.filter(~Question.id.in_(previous_questions)).all()

      else:
        questions_data = Question.query.filter(Question.category == quiz_category['id']).filter(~Question.id.in_(previous_questions)).all()

      # format the questions_data to a list
      questions_list =[Question.format(question) for question in questions_data]

      # Check if there is questions, if not set the questins value to None
      if questions_list:
        question = random.choice(questions_list)
      else:
        question = None

      return jsonify({
          'success': True,
          'question': question,
      })

    except:
      print(sys.exc_info())
      abort(422)

  '''
  @TODO: ✅
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422


  return app