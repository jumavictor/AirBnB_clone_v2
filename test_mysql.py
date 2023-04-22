#!/usr/bin/python3
"""
Example unittest for testing MySQL database interaction.

This script demonstrates how to use the unittest module to test a MySQL database.
It creates a new table in a test database, inserts a record into it, and then checks
that the record was successfully inserted.

Author: VictorJuma
Date: 2023-04-20
"""

import unittest
import mysql.connector

class TestMySQL(unittest.TestCase):

    def setUp(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="test_user",
            password="password",
            database="test_db"
        )
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

    def tearDown(self):
        self.cursor.execute("DROP TABLE test_table")
        self.db.close()

    def test_insert_record(self):
        # Get the number of records before inserting
        self.cursor.execute("SELECT COUNT(*) FROM test_table")
        initial_count = self.cursor.fetchone()[0]

        # Insert a new record
        self.cursor.execute("INSERT INTO test_table (name) VALUES ('John')")

        # Get the number of records after inserting
        self.cursor.execute("SELECT COUNT(*) FROM test_table")
        final_count = self.cursor.fetchone()[0]

        # Check that the difference is 1
        self.assertEqual(final_count - initial_count, 1)

if __name__ == '__main__':
    unittest.main()
