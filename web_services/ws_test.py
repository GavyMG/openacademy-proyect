import functools
import xmlrpclib
HOST = 'localhost'
PORT = 8069
DB = 'odoo_curso'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print "Logged in as %s (uid:%d)" % (USER,uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
model = 'openacademy.session'
domain = []
method_name = 'search_read'
sessions = call(model,method_name, domain, ['name','seats'])
for session in sessions:
    print "Session %s (%s seats)" % (session['name'], session['seats'])

# 3.search
#domain = [('name', '=','Course 0')] 
#course_ids = call('openacademy.course', 'search', domain)
#print "course_id", course_ids 
#course_id = course_ids[0]

# 3.create a new session for the "Functional" course
course_id = call('openacademy.course', 'search', [('name','ilike','Functional')])[0]
session_id = call('openacademy.session', 'create', {
    'name' : 'My session',
    'course_id' : course_id,
})

# 4.create a new session
session_id = call('openacademy.session', 'create', {
    'name' : 'My session',
    'course_id' : course_id,
})

# 4.create a new course
#session_id = call('openacademy.course', 'create', {
#    'name' : 'Funtional',
#})

# 5.many2many
#para concatenar 4 
#'attendee_ids':[(4, responsible_id)],
