import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "192.168.1.20:5432", self.database_name
            )
        
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        
        '''data to test insertion of new data.
        # reinsert 23 data:  id, question, answer, difficulty, category) 
                     values (23, 'Which dung beetle was worshipped by the ancient Egyptians?', 'Scarab', 4, 4);'''
        self.new_question = {
            #"id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?",
            "answer": "Scarab",
            "difficulty": 4,
            "category": 4
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    '''Test deletion of question and error if not exist.'''
    # def test_delete_questions(self):
    #     '''Test deletion of question.'''
    #     res = self.client().delete("/questions/23")
    #     data = json.loads(res.data)

    #     with self.app.app_context():
    #         question = Question.query.filter(Question.id == 23).one_or_none()
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 23)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        '''Test deletion of question failure due to not exist.'''
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


    '''Test creating new question and error if not allowed'''
    def test_create_new_question(self):
        '''Test create new question.'''
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])
    
    def test_405_if_question_creation_not_allowed(self):
        '''Test post Not allowed'''
        res = self.client().post("/questions/10000", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()



#########################
# Start over with new db
#########################
'''
# in psql session
drop database trivia_test;
create database trivia_test;

# from bash
psql -U postgres -h 192.168.1.20 -p 5432 -d trivia_test -f mytriviadump.sql
'''