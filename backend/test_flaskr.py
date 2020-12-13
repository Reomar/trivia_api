import os
from re import search
import unittest
import json
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = database_path = "postgres://{}:{}@{}/{}".format('omar', 'reomar15', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.test_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
    Test for /categories GET endpoint
    ---------------------------------
    '''
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])


    '''
    Tests for /questions GET endpoint
    ---------------------------------
    '''
    def test_get_all_questions(self):
        """Test /questions endpoint that retrives all the questions """

        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertNotEqual(data['total_questions'], 0)
        self.assertTrue(data['categories'])

    def test_404_if_get_questions_dosent_exist(self):
        """Test /questions endpoint when page dosen't exist (404) """

        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    '''
    Tests for /questions/<id> DELETE endpoint
    -----------------------------------------
    '''
    def test_delete_question(self):
        ''' Test /question/<id> endpoint that deletes question using id'''
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question_dosent_exist(self):
        """Test /question/<id> endpoint when question dosen't exist (404) """

        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    '''
    Test for /questions POST endpoint
    ---------------------------------
    '''
    def test_insert_new_question(self):
        """Test inserting new question to /question endpoint"""

        test_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }

        question_count_before = Question.query.count()

        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        question_count_after = Question.query.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question_count_after , question_count_before + 1)

    def test_422_missing_data_insert_new_question(self):
        """Test getting 422 error when posting to /questions with missing data"""

        test_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
        }

        question_count_before = Question.query.count()

        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        question_count_after = Question.query.count()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(question_count_after , question_count_before)

    def test_422_None_value_data_insert_new_question(self):
        """Test getting 422 error when posting to /questions with data of a value of None"""
        test_question = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1
        }

        question_count_before = Question.query.count()

        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        question_count_after = Question.query.count()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(question_count_after , question_count_before)


    '''
    Tests for /questions/search endpoint (POST)
    --------------------------------------------
    '''

    def test_search_questions(self):
        '''Test search for questions '''

        search_term = {'searchTerm': 'Tom Hanks'}

        # Send search Term to the endpoint
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertNotEqual(data['total_questions'], 0)

    def test_404_search_question_not_found(self):
        '''Test 404 error when search for questions in not found'''

        search_term = {'searchTerm': ",Q=_,2wDi>1+33NWC:]+|E~6vuD%Xx"}

        # Send search Term to the endpoint
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''
    Tests for categories/<id>/questions endpoint (GET)
    '''

    def test_get_questions_sorted_by_category(self):
        ''' Test the categories/<id>/questions endpoint to get questions sorted by category'''

        # send a get request to the endpoint
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertNotEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], 1)

    def test_404_get_questions_sorted_by_category_not_found(self):
        ''' Test getting erorr (404) from categories/<id>/questions endpoint when id not found'''

        # send a get request to the endpoint
        res = self.client().get('/categories/99999999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    '''
    Tests for categories/<id>/questions endpoint (GET)
    '''

    def test_get_quiz_question(self):
        ''' Test getting a qustion from /quizzes that wasent sent befor'''
        sent_request = {
            'previous_questions': [],
            'quiz_category':  {'type': "click", 'id': 0}
        }

        res = self.client().post('/quizzes', json = sent_request)
        data =  json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_get_quiz_question_missing_request(self):
        ''' Test getting a qustion from /quizzes that wasent sent befor'''
        sent_request = {
            'quiz_category':  {'type': "click", 'id': 0}
        }

        res = self.client().post('/quizzes', json = sent_request)
        data =  json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()