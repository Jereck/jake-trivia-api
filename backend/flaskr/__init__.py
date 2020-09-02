import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS Setup to allow '*'
  CORS(app, resources={'/': {'origins': '*'}})

  # after_request to set all Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  """
  [GET] all available categories

  Also formats the returned json to match the front end
  """
  @app.route('/categories')
  def get_all_categories():
    try:
      categories = Category.query.all()

      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type

      return jsonify({
        'success': True,
        'categories': categories_dict,
      })
    except:
      abort(500)

  """
  [GET] all questions - 10 questions per page
  """
  @app.route('/questions')
  def get_all_questions():
    # Setup all necessary requirements
    selection = Question.query.order_by(Question.id).all()
    total_questions = len(selection)
    categories = Category.query.order_by(Category.id).all()

    # Put questions in paginated form
    current_questions = paginate_questions(request, selection)

    # Return a 404 error if no questions are found
    if len(current_questions) == 0:
      abort(404)

    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': categories_dict
    })


  """
  [DELETE] question by it's id
  """
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      # Finds the question by it's id
      question = Question.query.filter(Question.id == question_id).one_or_none()

      # If there is no question found, it aborts with a 404 not found
      if question is None:
        abort(404)

      # Else, it deletes the question
      question.delete()

      return jsonify({
        'success': True,
        'message': 'Question successfully deleted',
      })
    except:
      abort(422)


  """
  [POST] - Create's a question from submitted form
  """
  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()

    # Converts data from json data
    question = data.get('question', '')
    answer = data.get('answer', '')
    difficulty = data.get('difficulty', '')
    category = data.get('category', '')

    if question == '' or answer == '' or difficulty == '' or category == '':
      abort(422)
    
    try:
      # Attempts to create the new question
      question = Question(
        question=question,
        answer=answer,
        difficulty=difficulty,
        category=category
      )
      
      # Saves question to the db
      question.insert()

      return jsonify({
        'success': True,
        'message': 'Your question was saved successfully!'
      })
    except:
      abort(422)

  """
  [POST] - Searches for questions based off of searchTerm variable on front end.
  """
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm', '')

    # Checks for search term or aborts
    if search_term == '':
      abort(422)

    try:
      # Get all questions based on search term
      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()

      # If 0 questions are returned, abort
      if len(selection) == 0:
        abort(404)

      questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(Question.query.all())
      })
    
    except:
      abort(404)

  """
  [GET] - Get's questions based on their category
  """
  @app.route('/categories/<int:cat_id>/questions')
  def get_questions_per_category(cat_id):
    # Get the category based on it's id
    category = Category.query.filter_by(id=cat_id).one_or_none()

    # Makes sure there is a category or aborts
    if category is None:
      abort(422)

    # Get's questions based on category ID
    cat_questions = Question.query.filter_by(category = cat_id).all()

    questions = paginate_questions(request, cat_questions)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(cat_questions),
      'current_category': category.type
    })


  """
  [POST] - Enables gameplay and random next questions
  """
  @app.route('/quizzes', methods=['POST'])
  def questions_to_play_quiz():
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')

    # Abort is quiz or previous question is empty
    if quiz_category is None or previous_questions is None:
      abort(400)

    # If default category, return all
    if quiz_category['id'] == 0:
      questions = Question.query.all()
    # Else return specific category questions
    else:
      questions = Question.query.filter_by(category=quiz_category['id']).all()

    # Generates random question
    def gen_random_question():
      return questions[random.randint(0, len(questions) - 1)]

    # Now, need to get the next question randomly
    next_question = gen_random_question()

    # Create boolean to ensure the question is not repeated
    same_question = True

    while same_question:
      if next_question.id in previous_questions:
        next_question = gen_random_question()
      else:
        same_question = False
    
    return jsonify({
      'success': True,
      'question': next_question.format()
    })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405
    
  @app.errorhandler(500)
  def internal_service_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal service error has occured"
    })
  
  return app

    