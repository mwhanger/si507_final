import sqlite3
import unittest
from SI507_final import *

class FinProjDBTests(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect("chroniclingamerica.sqlite")
        self.cur = self.conn.cursor()

    #verifying a one-to-many relationship in my database
    #Can't verify many-to-many -- all many-to-many values in my data have nulls as possible values
    def test_many(self):
        self.cur.execute("Select * from Paper where publisher_id is null")
        data = self.cur.fetchall()
        self.assertFalse(data,"Testing that all papers have a publisher assigned.")

    #verifying that all papers are unique by confirming that no duplicate lccn numbers are present
    def test_lccn(self):
        self.cur.execute("select count(lccn) from Paper group by lccn having count(lccn) > 1")
        data = self.cur.fetchall()
        self.assertFalse(data,"Testing that all LCCN numbers are unique.")

    def tearDown(self):
    	self.conn.commit()
    	self.conn.close()

class FinProjVarTests(unittest.TestCase):

    #Defining an object of the class paper to verify the model works
    def setUp(self):
        self.paper = Paper(title="Test Paper")

    def test_paper_class(self):
        self.assertIsInstance(self.paper, Paper, "Testing that Paper class in models file configured correctly and returns an instance of Paper.")

    def test_flask_app(self):
        self.assertIsInstance(app, Flask, "Testing that the app variable is a successfully defined Flask app.")

    def tearDown(self):
        del(self.paper)


if __name__ == '__main__':
    unittest.main(verbosity=2)
