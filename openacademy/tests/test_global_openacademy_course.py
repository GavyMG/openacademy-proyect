# -*- coding: utf-8 -*-
from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    """
    Global test to openacademy course model.
    test create course and trigger constraints.
    """

    # Method seudo-constructor of test setUp
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'hello world'
        self.course = self.env['openacademy.course']
    # Method of class that is not test
    def create_course(self, name, description, responsible_id):
        course_id = self.course.create({
            'name': name,
            'description': description,
            'responsible_id': responsible_id,
        })
        return course_id
        
    # Method of test startswith 'def test_*(self):'
    @mute_logger('openerp.sql_db')
    def test_10_same_name_description(self):
        """
        Test create a course with same name and description.
        to test constraint of name different to description.
        """
        # Error raised expected with message
        with self.assertRaisesRegexp(IntegrityError, 
                'new row for relation "openacademy_course" violates check'
                ' constraint "openacademy_course_name_description_check"'):
            # create a course to raise error
            self.create_course('test', 'test', None)

    @mute_logger('openerp.sql_db')
    def test_20_two_course_same_name(self):
        """
        Test to create two course with same name
        To raise constraint of unique name
        """
        new_id = self.create_course('test1', 'test_description', None)
        print "new_id", new_id
        with self.assertRaisesRegexp(IntegrityError,
                'duplicate key value violates unique constraint'
                ' "openacademy_course_name_unique"'): 
            new_id2 = self.create_course('test1', 'test_description', None)

    def test_15_duplicate_course(self):
        """
        Test to duplicate a course and check that works fine
        """
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print "course_id", course_id
