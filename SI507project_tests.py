import sqlite3
import unittest

class FinProjTests(unittest.TestCase):

    def connect(self):
        self.conn = sqlite3.connect("chroniclingamerica.sqlite")
        self.cur = self.conn.cursor()

    #verifying the many-to-many relationships in my database
    def test_many(self):
        self.cur.execute("Select * from Paper left join states on Paper.id = states.paper_id where states.state_id is null")
        data = self.cur.fetchall()
        self.assertFalse(data,"Testing that all papers have at least one state assigned.")

    #verifying that all papers are unique by confirming that no duplicate lccn numbers are present
    def test_lccn(self):
        self.cur.execute("select count(lccn) from Paper group by lccn having count(lccn) > 1")
        data = self.cur.fetchall()
        self.assertFalse(data,"Testing that all LCCN numbers are unique.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
