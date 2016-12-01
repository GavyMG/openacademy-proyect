# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class GlobalTestOpenAcademySession(TransactionCase):
    """
    Global test to openacademy session model
    """

    # Seudo-constructor of test setUp
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner_vauxoo = self.env.ref('base.res_partner_23')
        self.partner_attende = self.env.ref('base.res_partner_5')
        self.course_0 = self.env.ref('openacademy.course0')

    # Generic methods

    # Test methods
    def test_10_instructor_is_attende(self):
        """
        Check that raise of 'A session's instructor can't be an attendee
        """
        with self.assertRaisesRegexp(
                ValidationError,
                "A session's instructor can't be an attendee"):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': self.course_0.id
                })

    def test_20_wkf_done(self):
        session_test = self.session.create({
            'name': 'Session test 1',
            'seats': 2,
            'instructor_id': self.partner_vauxoo.id,
            'attendee_ids': [(6, 0, [self.partner_attende.id])],
            'course_id': self.course_0.id
            })
        # Check initial state
        self.assertEqual(session_test.state, 'draft',
                         'Initial state should be in "draft"')
        # Change next state and check it
        session_test.signal_workflow('confirm')
        self.assertEqual(session_test.state, 'confirmed',
                         "Signal confirm don't work OK")
        # Change next state and check it
        session_test.signal_workflow('done')
        self.assertEqual(session_test.state, 'done',
                         "Signal confirm don't work OK")
        # Please don't use
        # self.env.cr.commit()    # Just to test the data generated by test.
