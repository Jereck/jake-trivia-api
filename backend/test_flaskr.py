import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

# Creates a test question and answer to be played with in test cases
def generate_test_question():
  question = Question(
    question='Test Question',
    answer='42',
    difficulty=1,
    category='1'
  )
  question.insert()

  return question.id

class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "trivia_test"
    self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'Stella1011!', 'localhost:5432', self.database_name)
    
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
  
  def tearDown(self):
    """Executed after reach test"""
    pass

  """
  Route: /categories
  Method: get_all_categories()
  """
  def test_get_all_categories(self):
    response = self.client().get('/categories')
    data = json.loads(response.data)

    # Makes assertions on each part of the response
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])
    self.assertEqual(len(data['categories']), 6)
  
  """
  Route: /questions
  Method: get_all_questions()
  """
  def test_get_all_questions(self):
    response = self.client().get('/questions')
    data = json.loads(response.data)

    # Makes assertions on each part of the response
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions'])
    self.assertTrue(data['categories'])
    self.assertTrue(data['total_questions'])
    self.assertEqual(len(data['questions']), 10)

  """
  Route: /questions?page=XXXXX
  Method: get_all_questions()
  """
  def test_get_all_questions_out_of_bounds(self):
    response = self.client().get('/questions?page=1000')
    data = json.loads(response.data)

    # Makes assertions on each part of the ERROR response
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  """
  Route: /questions/<int:question_id>
  Method: delete_question(question_id)
  """
  def test_delete_question_success(self):
    test_question_id = generate_test_question()

    # Calls the response based off the test question id
    response = self.client().delete('/questions/{}'.format(test_question_id))
    data = json.loads(response.data)

    # Make assertions to make sure question no longer exists
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['message'], "Question successfully deleted")

  """
  Route: /questions/<int:question_id> - where ID does not exist
  Method: delete_question(question_id)
  """
  def test_delete_question_no_id(self):
    response = self.client().delete('/questions/123456')
    data = json.loads(response.data)

    # Make assertions to make sure question no longer exists
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], "unprocessable")

  """
  Route: /questions
  Method: create_question()
  """
  def test_create_question(self):
    test_question = {
      'question': 'This is a silly test question',
      'answer': 'That is not a question',
      'difficulty': 1,
      'category': 5
    }

    response = self.client().post('/questions', json=test_question)
    data = json.loads(response.data)

    # Make assertions to make sure the response comes back correctly
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['message'], 'Your question was saved successfully!')

  """
  Route: /questions
  Method: create_question()
  """
  def test_create_empty_question(self):
    test_question = {
      'question': '',
      'answer': '',
      'difficulty': 1,
      'category': 1
    }

    response = self.client().post('/questions', json=test_question)
    data = json.loads(response.data)

    # Make assertions to make sure the ERROR response comes back correctly
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  """
  Route: /questions/search
  Method: search_questions()
  """
  def test_search_questions(self):
    test_search_term = {
      'searchTerm': 'title'
    }

    response = self.client().post('/questions/search', json=test_search_term)
    data = json.loads(response.data)

    # Make Assertions to test search response
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(len(data['questions']), 2)

  """
  Route: /questions/search
  Method: search_questions() - empty search string
  """
  def test_empty_search_questions(self):
    test_search_term = {
      'searchTerm': ''
    }

    response = self.client().post('/questions/search', json=test_search_term)
    data = json.loads(response.data)

    # Make Assertions to test search response error
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  """
  Route: /questions/search
  Method: search_questions() - search term not found
  """
  def test_empty_search_questions(self):
    test_search_term = {
      'searchTerm': 'wasdkeyboard1234'
    }

    response = self.client().post('/questions/search', json=test_search_term)
    data = json.loads(response.data)

    # Make Assertions to test search response error
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  """
  Route: /categories/<int:cat_id>/questions
  Method: get_questions_per_category(cat_id)
  """
  def test_get_questions_per_category(self):
    response = self.client().get('/categories/1/questions')
    data = json.loads(response.data)

    # Make assertions for successful json responses
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotEqual(len(data['questions']), 0)
    self.assertEqual(data['current_category'], 'Science')

  """
  Route: /categories/<int:cat_id>/questions
  Method: get_questions_per_category(cat_id) - category does not exist (dne)
  """
  def test_get_questions_per_category_dne(self):
    response = self.client().get('/categories/1234/questions')
    data = json.loads(response.data)

    # Make assertions for successful json responses
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  """
  Route: /quizzes
  Method: questions_to_play_quiz()
  """
  def test_questions_to_play_quiz(self):
    quiz_data = {
      'previous_questions': [2,5],
      'quiz_category': {
        'type': 'History',
        'id': 4
      }
    }

    response = self.client().post('/quizzes', json=quiz_data)
    data = json.loads(response.data)

    # Make assertions for testing proper responses
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['question'])

    # Test to make sure previous questions don't come back
    self.assertNotEqual(data['question']['id'], 2)
    self.assertNotEqual(data['question']['id'], 5)

    # Assert test category
    self.assertEqual(data['question']['category'], 4)

  """
  Route: /quizzes
  Method: questions_to_play_quiz() - no data
  """
  def test_questions_to_play_quiz_blank(self):
    response = self.client().post('/quizzes', json={})
    data = json.loads(response.data)

    # Make assertions to test error response
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()