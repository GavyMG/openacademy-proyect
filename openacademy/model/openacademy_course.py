from openerp import models, fields
'''
This module create model of Course
'''


class Course(models.Model):
    '''
    this class model of Course
    '''
    _name = 'openacademy.course'  # Model odoo name

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")
