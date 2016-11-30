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
    def test_01_same_name_description(self):
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
